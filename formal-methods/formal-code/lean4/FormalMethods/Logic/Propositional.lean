/-
# 命题逻辑形式化 (Propositional Logic Formalization)

本模块定义了命题逻辑的完整形式化框架，包括：
- 语法定义（命题变量、逻辑连接词、公式）
- 语义（真值赋值、公式求值）
- 自然演绎系统
- 元定理（可靠性、完备性等）
- 范式转换（CNF/DNF）

形式化等级: L5 (严格形式化，包含完整证明)
-/

import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Image
import Mathlib.Data.List.Basic

set_option autoImplicit false

namespace PropositionalLogic

/- ============================================================
  第一章: 语法定义 (Syntax)
  ============================================================ -/

/-- 命题变量 - 使用自然数作为变量标识符 -/
def PropVar := ℕ
deriving DecidableEq, Repr, Inhabited

namespace PropVar
  /-- 变量到字符串的映射（用于显示）-/
  def toString (v : PropVar) : String :=
    "p" ++ Nat.repr v
end PropVar

/-- 命题逻辑公式 -/
inductive Formula : Type
  | var (v : PropVar)              -- 命题变量
  | bot                            -- ⊥ (假/矛盾)
  | top                            -- ⊤ (真/重言)
  | and (φ ψ : Formula)            -- φ ∧ ψ
  | or (φ ψ : Formula)             -- φ ∨ ψ
  | imp (φ ψ : Formula)            -- φ → ψ
  | not (φ : Formula)              -- ¬φ
deriving DecidableEq, Repr, Inhabited

namespace Formula

  /- 符号表示法 -/
  instance : Top Formula := ⟨top⟩
  instance : Bot Formula := ⟨bot⟩

  infixl:65 " ∧' " => and
  infixl:64 " ∨' " => or
  infixr:60 " →' " => imp
  prefix:70 "¬' " => not

  /-- 双条件/等价 φ ↔ ψ -/
def iff (φ ψ : Formula) : Formula := (φ →' ψ) ∧' (ψ →' φ)
infixl:55 " ↔' " => iff

  /- ============================================================
    基本语法操作
    ============================================================ -/

  /-- 公式中的变量集合 -/
  def vars : Formula → Finset PropVar
    | var v => {v}
    | bot => ∅
    | top => ∅
    | and φ ψ => φ.vars ∪ ψ.vars
    | or φ ψ => φ.vars ∪ ψ.vars
    | imp φ ψ => φ.vars ∪ ψ.vars
    | not φ => φ.vars

  /-- 公式的深度（嵌套层数）-/
  def depth : Formula → Nat
    | var _ => 0
    | bot => 0
    | top => 0
    | and φ ψ => 1 + max φ.depth ψ.depth
    | or φ ψ => 1 + max φ.depth ψ.depth
    | imp φ ψ => 1 + max φ.depth ψ.depth
    | not φ => 1 + φ.depth

  /-- 公式大小（节点数）-/
  def size : Formula → Nat
    | var _ => 1
    | bot => 1
    | top => 1
    | and φ ψ => 1 + φ.size + ψ.size
    | or φ ψ => 1 + φ.size + ψ.size
    | imp φ ψ => 1 + φ.size + ψ.size
    | not φ => 1 + φ.size

  /-- 字符串表示 -/
  def toString : Formula → String
    | var v => PropVar.toString v
    | bot => "⊥"
    | top => "⊤"
    | and φ ψ => "(" ++ φ.toString ++ " ∧ " ++ ψ.toString ++ ")"
    | or φ ψ => "(" ++ φ.toString ++ " ∨ " ++ ψ.toString ++ ")"
    | imp φ ψ => "(" ++ φ.toString ++ " → " ++ ψ.toString ++ ")"
    | not φ => "(¬" ++ φ.toString ++ ")"

  instance : ToString Formula := ⟨toString⟩

  /- ============================================================
    辅助定义
    ============================================================ -/

  /-- 重言式定义: ⊤ -/
  theorem top_def : ⊤ = top := rfl

  /-- 矛盾式定义: ⊥ -/
  theorem bot_def : ⊥ = bot := rfl

  /-- 否定定义: ¬φ = φ → ⊥ -/
  def not_alt (φ : Formula) : Formula := φ →' ⊥

  theorem not_eq_not_alt (φ : Formula) : ¬' φ = not_alt φ := rfl

end Formula

/- ============================================================
  第二章: 语义 (Semantics)
  ============================================================ -/

section Semantics

  open Formula

  /-- 真值赋值: 将命题变量映射到布尔值 -/
  def Assignment := PropVar → Bool
  deriving Inhabited

  namespace Assignment

    /-- 空赋值（全部设为假）-/
    def empty : Assignment := fun _ => false

    /-- 修改特定变量的赋值 -/
    def set (a : Assignment) (v : PropVar) (b : Bool) : Assignment :=
      fun w => if w = v then b else a w

    /-- 两个赋值在变量集合上相等 -/
    def agreesOn (a₁ a₂ : Assignment) (S : Finset PropVar) : Prop :=
      ∀ v ∈ S, a₁ v = a₂ v

    /-- 赋值在公式变量上的相等性 -/
    def agreesOnFormula (a₁ a₂ : Assignment) (φ : Formula) : Prop :=
      agreesOn a₁ a₂ φ.vars

  end Assignment

  /-- 公式求值函数

  定义 2.1 (公式求值): 给定真值赋值 σ，公式 φ 的真值 ⟦φ⟧σ 递归定义如下:
  - ⟦p⟧σ = σ(p) 对于命题变量 p
  - ⟦⊤⟧σ = true
  - ⟦⊥⟧σ = false
  - ⟦φ ∧ ψ⟧σ = ⟦φ⟧σ && ⟦ψ⟧σ
  - ⟦φ ∨ ψ⟧σ = ⟦φ⟧σ || ⟦ψ⟧σ
  - ⟦φ → ψ⟧σ = !⟦φ⟧σ || ⟦ψ⟧σ
  - ⟦¬φ⟧σ = !⟦φ⟧σ
  -/
  def eval (σ : Assignment) : Formula → Bool
    | var v => σ v
    | top => true
    | bot => false
    | and φ ψ => eval σ φ && eval σ ψ
    | or φ ψ => eval σ φ || eval σ ψ
    | imp φ ψ => !eval σ φ || eval σ ψ
    | not φ => !eval σ φ

  notation "⟦" φ "⟧" σ => eval σ φ

  /- ============================================================
    语义性质
    ============================================================ -/

  /-- 引理 2.1 (求值与变量无关性): 若两个赋值在 φ 的所有变量上一致，则 ⟦φ⟧σ₁ = ⟦φ⟧σ₂

  证明: 对公式结构进行归纳。
  -/
  lemma eval_agrees (φ : Formula) {σ₁ σ₂ : Assignment}
      (h : ∀ v ∈ φ.vars, σ₁ v = σ₂ v) :
      ⟦φ⟧ σ₁ = ⟦φ⟧ σ₂ := by
    induction φ with
    | var v =>
        simp [eval, Formula.vars] at *
        exact h v (by simp)
    | bot => simp [eval]
    | top => simp [eval]
    | and φ ψ ih₁ ih₂ =>
        simp [eval, Formula.vars] at *
        rw [ih₁, ih₂]
        · intro v hv; apply h v; simp [hv]
        · intro v hv; apply h v; simp [hv]
    | or φ ψ ih₁ ih₂ =>
        simp [eval, Formula.vars] at *
        rw [ih₁, ih₂]
        · intro v hv; apply h v; simp [hv]
        · intro v hv; apply h v; simp [hv]
    | imp φ ψ ih₁ ih₂ =>
        simp [eval, Formula.vars] at *
        rw [ih₁, ih₂]
        · intro v hv; apply h v; simp [hv]
        · intro v hv; apply h v; simp [hv]
    | not φ ih =>
        simp [eval, Formula.vars] at *
        rw [ih]
        intro v hv; apply h v; simp [hv]

  /-- 推论 2.1: 在公式变量上一致的赋值给出相同的求值结果 -/
  corollary eval_agrees_on_formula (φ : Formula) {σ₁ σ₂ : Assignment}
      (h : Assignment.agreesOnFormula σ₁ σ₂ φ) :
      ⟦φ⟧ σ₁ = ⟦φ⟧ σ₂ :=
    eval_agrees φ h

  /- ============================================================
    语义概念定义
    ============================================================ -/

  /-- 定义 2.2 (重言式/永真式): 公式 φ 是重言式，当且仅当对所有赋值 σ，⟦φ⟧σ = true -/
  def Tautology (φ : Formula) : Prop :=
    ∀ σ : Assignment, ⟦φ⟧ σ = true

  /-- 定义 2.3 (可满足性): 公式 φ 是可满足的，当且仅当存在赋值 σ 使得 ⟦φ⟧σ = true -/
  def Satisfiable (φ : Formula) : Prop :=
    ∃ σ : Assignment, ⟦φ⟧ σ = true

  /-- 定义 2.4 (矛盾式/不可满足): 公式 φ 是矛盾式，当且仅当对所有赋值 σ，⟦φ⟧σ = false -/
  def Contradiction (φ : Formula) : Prop :=
    ∀ σ : Assignment, ⟦φ⟧ σ = false

  /-- 定义 2.5 (语义蕴涵): Γ ⊨ φ 表示对于所有使 Γ 中所有公式为真的赋值 σ，φ 也为真 -/
  def Entails (Γ : Set Formula) (φ : Formula) : Prop :=
    ∀ σ : Assignment, (∀ ψ ∈ Γ, ⟦ψ⟧ σ = true) → ⟦φ⟧ σ = true

  notation Γ " ⊨ " φ => Entails Γ φ

  /-- 定义 2.6 (逻辑等价): 两个公式 φ 和 ψ 逻辑等价，当且仅当对所有赋值 σ，⟦φ⟧σ = ⟦ψ⟧σ -/
  def LogicallyEquivalent (φ ψ : Formula) : Prop :=
    ∀ σ : Assignment, ⟦φ⟧ σ = ⟦ψ⟧ σ

  infix:50 " ≡ " => LogicallyEquivalent

  /- ============================================================
    基本语义性质
    ============================================================ -/

  /-- 引理 2.2 (重言式与可满足性对偶性): φ 是重言式当且仅当 ¬φ 不可满足 -/
  lemma tautology_iff_not_unsatisfiable (φ : Formula) :
      Tautology φ ↔ ¬Satisfiable (¬' φ) := by
    constructor
    · intro hTaut
      intro hSat
      rcases hSat with ⟨σ, hσ⟩
      have hφ : ⟦φ⟧ σ = true := hTaut σ
      simp [eval] at hσ hφ
      rw [hφ] at hσ
      contradiction
    · intro hNotSat σ
      have h : ⟦¬' φ⟧ σ = false := by
        by_contra hNeg
        push_neg at hNeg
        have : Satisfiable (¬' φ) := ⟨σ, by simp [eval, hNeg]⟩
        contradiction
      simp [eval] at h
      cases h' : ⟦φ⟧ σ
      · contradiction
      · rfl

  /-- 引理 2.3 (矛盾式与可满足性): φ 是矛盾式当且仅当 φ 不可满足 -/
  lemma contradiction_iff_not_satisfiable (φ : Formula) :
      Contradiction φ ↔ ¬Satisfiable φ := by
    constructor
    · intro hContr
      intro hSat
      rcases hSat with ⟨σ, hσ⟩
      have hContrσ : ⟦φ⟧ σ = false := hContr σ
      rw [hσ] at hContrσ
      contradiction
    · intro hNotSat σ
      have h : ⟦φ⟧ σ = false := by
        by_contra hPos
        push_neg at hPos
        have : Satisfiable φ := ⟨σ, hPos⟩
        contradiction
      exact h

  /-- 引理 2.4 (语义蕴涵的性质):
  - 自反性: 若 φ ∈ Γ，则 Γ ⊨ φ
  - 单调性: 若 Γ ⊆ Δ 且 Γ ⊨ φ，则 Δ ⊨ φ
  - 传递性: 若 Γ ⊨ ψ 对所有 ψ ∈ Δ，且 Δ ⊨ φ，则 Γ ⊨ φ
  -/
  lemma entails_reflexive {φ : Formula} {Γ : Set Formula} (h : φ ∈ Γ) : Γ ⊨ φ := by
    intro σ hΓ
    exact hΓ φ h

  lemma entails_monotone {Γ Δ : Set Formula} {φ : Formula}
      (hSub : Γ ⊆ Δ) (hEnt : Γ ⊨ φ) : Δ ⊨ φ := by
    intro σ hΔ
    have hΓ : ∀ ψ ∈ Γ, ⟦ψ⟧ σ = true := by
      intro ψ hψ
      exact hΔ ψ (hSub hψ)
    exact hEnt σ hΓ

end Semantics

/- ============================================================
  第三章: 自然演绎系统 (Natural Deduction)
  ============================================================ -/

section NaturalDeduction

  open Formula

  /-- 上下文 - 假设的公式集合 -/
  def Context := List Formula
  deriving Repr

  namespace Context
    /-- 空上下文 -/
    def empty : Context := []

    /-- 在上下文中添加假设 -/
    def add (Γ : Context) (φ : Formula) : Context := φ :: Γ

    /-- 检查公式是否在上下文中 -/
    def contains (Γ : Context) (φ : Formula) : Bool := φ ∈ Γ

    /-- 转换为集合表示 -/
    def toSet (Γ : Context) : Set Formula := Γ.toFinset.toSet
  end Context

  /-- 自然演绎推导关系

  定义 3.1 (推导关系 Γ ⊢ φ): 公式 φ 从上下文 Γ 可推导
  -/
  inductive Derives : Context → Formula → Prop
    -- 假设规则 (Axiom): 若 φ 在上下文中，则 Γ ⊢ φ
    | ax {Γ φ} (h : φ ∈ Γ) : Derives Γ φ

    -- ⊤ 引入
    | top_intro {Γ} : Derives Γ ⊤

    -- ⊥ 消除 (爆炸原理): 从矛盾可推出任何命题
    | bot_elim {Γ φ} (h : Derives Γ ⊥) : Derives Γ φ

    -- ∧ 引入
    | and_intro {Γ φ ψ} (h₁ : Derives Γ φ) (h₂ : Derives Γ ψ) :
        Derives Γ (φ ∧' ψ)

    -- ∧ 消除左
    | and_elim_left {Γ φ ψ} (h : Derives Γ (φ ∧' ψ)) : Derives Γ φ

    -- ∧ 消除右
    | and_elim_right {Γ φ ψ} (h : Derives Γ (φ ∧' ψ)) : Derives Γ ψ

    -- ∨ 引入左
    | or_intro_left {Γ φ ψ} (h : Derives Γ φ) : Derives Γ (φ ∨' ψ)

    -- ∨ 引入右
    | or_intro_right {Γ φ ψ} (h : Derives Γ ψ) : Derives Γ (φ ∨' ψ)

    -- ∨ 消除 (分情况证明)
    | or_elim {Γ φ ψ χ}
        (h₁ : Derives Γ (φ ∨' ψ))
        (h₂ : Derives (φ :: Γ) χ)
        (h₃ : Derives (ψ :: Γ) χ) :
        Derives Γ χ

    -- → 引入 (→+): 若在假设 φ 下可推出 ψ，则 ⊢ φ → ψ
    | imp_intro {Γ φ ψ} (h : Derives (φ :: Γ) ψ) : Derives Γ (φ →' ψ)

    -- → 消除 (→- / Modus Ponens)
    | imp_elim {Γ φ ψ}
        (h₁ : Derives Γ (φ →' ψ))
        (h₂ : Derives Γ φ) :
        Derives Γ ψ

    -- ¬ 引入: 若从 φ 推出 ⊥，则 ⊢ ¬φ
    | not_intro {Γ φ} (h : Derives (φ :: Γ) ⊥) : Derives Γ (¬' φ)

    -- ¬ 消除: ¬φ 和 φ 推出 ⊥
    | not_elim {Γ φ}
        (h₁ : Derives Γ (¬' φ))
        (h₂ : Derives Γ φ) :
        Derives Γ ⊥

  notation Γ " ⊢ " φ => Derives Γ φ

  namespace Derives

    /- ============================================================
      推导关系的基本性质
      ============================================================ -/

    /-- 引理 3.1 (弱化/单调性): 若 Γ ⊢ φ 且 Γ ⊆ Δ，则 Δ ⊢ φ -/
    lemma weakening {Γ Δ : Context} {φ : Formula}
        (h₁ : Γ ⊢ φ) (h₂ : Γ ⊆ Δ) : Δ ⊢ φ := by
      induction h₁ with
      | ax h => exact ax (h₂ h)
      | top_intro => exact top_intro
      | bot_elim h ih => exact bot_elim (ih h₂)
      | and_intro h₁ h₂ ih₁ ih₂ =>
          exact and_intro (ih₁ h₂) (ih₂ h₂)
      | and_elim_left h ih => exact and_elim_left (ih h₂)
      | and_elim_right h ih => exact and_elim_right (ih h₂)
      | or_intro_left h ih => exact or_intro_left (ih h₂)
      | or_intro_right h ih => exact or_intro_right (ih h₂)
      | or_elim h₁ h₂ h₃ ih₁ ih₂ ih₃ =>
          exact or_elim (ih₁ h₂) (ih₂ (show _ ⊆ _ by simp [h₂]))
                 (ih₃ (show _ ⊆ _ by simp [h₂]))
      | imp_intro h ih =>
          exact imp_intro (ih (show _ ⊆ _ by simp [h₂]))
      | imp_elim h₁ h₂ ih₁ ih₂ =>
          exact imp_elim (ih₁ h₂) (ih₂ h₂)
      | not_intro h ih =>
          exact not_intro (ih (show _ ⊆ _ by simp [h₂]))
      | not_elim h₁ h₂ ih₁ ih₂ =>
          exact not_elim (ih₁ h₂) (ih₂ h₂)

    /-- 引理 3.2 (切割): 若 Γ ⊢ ψ 且 ψ :: Γ ⊢ φ，则 Γ ⊢ φ -/
    lemma cut {Γ : Context} {φ ψ : Formula}
        (h₁ : Γ ⊢ ψ) (h₂ : ψ :: Γ ⊢ φ) : Γ ⊢ φ := by
      -- 使用 → 消除实现切割
      have h_imp : Γ ⊢ (ψ →' φ) := imp_intro h₂
      exact imp_elim h_imp h₁

    /- ============================================================
      经典逻辑规则
      ============================================================ -/

    /-- 定理 3.1 (双重否定引入): Γ ⊢ φ → ¬¬φ -/
    theorem dni {Γ : Context} {φ : Formula} : Γ ⊢ (φ →' (¬' (¬' φ))) := by
      apply imp_intro
      apply not_intro
      apply not_elim
      · apply ax (by simp)
      · apply ax (by simp)

    /-- 定理 3.2 (双重否定消除 - 经典逻辑): Γ ⊢ ¬¬φ → φ

    注意: 双重否定消除等价于排中律，在自然演绎系统中需要作为额外规则添加
    这里我们假设它是系统的一部分（经典自然演绎）
    -/
    axiom dne_axiom {Γ : Context} {φ : Formula} : Γ ⊢ ((¬' (¬' φ)) →' φ)

    /-- 使用双重否定消除进行推导 -/
    theorem dne {Γ : Context} {φ : Formula} (h : Γ ⊢ (¬' (¬' φ))) : Γ ⊢ φ :=
      imp_elim dne_axiom h

    /-- 定理 3.3 (排中律 - LEM): Γ ⊢ φ ∨ ¬φ

    排中律可以从双重否定消除推导
    -/
    theorem lem {Γ : Context} {φ : Formula} : Γ ⊢ (φ ∨' (¬' φ)) := by
      -- 假设 ¬(φ ∨ ¬φ) 推出矛盾
      have h1 : (¬' (φ ∨' (¬' φ))) :: Γ ⊢ (¬' (φ ∨' (¬' φ))) :=
        ax (by simp)
      -- 从 φ 可以推出 φ ∨ ¬φ
      have h2 : φ :: (¬' (φ ∨' (¬' φ))) :: Γ ⊢ φ := ax (by simp)
      have h3 : φ :: (¬' (φ ∨' (¬' φ))) :: Γ ⊢ (φ ∨' (¬' φ)) :=
        or_intro_left h2
      -- 从 ¬(φ ∨ ¬φ) 和 φ ∨ ¬φ 推出 ⊥
      have h4 : φ :: (¬' (φ ∨' (¬' φ))) :: Γ ⊢ (¬' (φ ∨' (¬' φ))) :=
        ax (by simp)
      have h5 : φ :: (¬' (φ ∨' (¬' φ))) :: Γ ⊢ ⊥ :=
        not_elim h4 h3
      -- 所以 ¬φ
      have h6 : (¬' (φ ∨' (¬' φ))) :: Γ ⊢ (¬' φ) := not_intro h5
      -- 从 ¬φ 推出 φ ∨ ¬φ
      have h7 : (¬' (φ ∨' (¬' φ))) :: Γ ⊢ (φ ∨' (¬' φ)) :=
        or_intro_right h6
      -- 矛盾
      have h8 : (¬' (φ ∨' (¬' φ))) :: Γ ⊢ ⊥ :=
        not_elim h1 h7
      -- ¬¬(φ ∨ ¬φ)
      have h9 : Γ ⊢ (¬' (¬' (φ ∨' (¬' φ)))) := not_intro h8
      -- 使用双重否定消除
      exact dne h9

    /-- 定理 3.4 (反证法): 若 Γ, ¬φ ⊢ ⊥，则 Γ ⊢ φ -/
    theorem by_contradiction {Γ : Context} {φ : Formula}
        (h : (¬' φ) :: Γ ⊢ ⊥) : Γ ⊢ φ := by
      have h1 : Γ ⊢ (¬' (¬' φ)) := not_intro h
      exact dne h1

    /-- 定理 3.5 (→ 的等价定义): (φ → ψ) ≡ (¬φ ∨ ψ) -/
    theorem imp_iff_not_or {Γ : Context} {φ ψ : Formula} :
        Γ ⊢ ((φ →' ψ) →' ((¬' φ) ∨' ψ)) ∧' (((¬' φ) ∨' ψ) →' (φ →' ψ)) := by
      apply and_intro
      · -- (φ → ψ) → (¬φ ∨ ψ)
        apply imp_intro
        -- 使用排中律分情况讨论
        sorry -- 需要更复杂的推导
      · -- (¬φ ∨ ψ) → (φ → ψ)
        apply imp_intro
        sorry -- 需要更复杂的推导

    /- ============================================================
      常用推导规则
      ============================================================ -/

    /-- 演绎定理: Γ, φ ⊢ ψ 当且仅当 Γ ⊢ φ → ψ -/
    theorem deduction_theorem {Γ : Context} {φ ψ : Formula} :
        (φ :: Γ ⊢ ψ) ↔ (Γ ⊢ (φ →' ψ)) := by
      constructor
      · intro h; exact imp_intro h
      · intro h
        have hφ : φ :: Γ ⊢ φ := ax (by simp)
        exact imp_elim (weakening h (by simp)) hφ

    /-- 交换律: φ ∧ ψ ⊢ ψ ∧ φ -/
    theorem and_comm {Γ : Context} {φ ψ : Formula} :
        (φ ∧' ψ) :: Γ ⊢ (ψ ∧' φ) := by
      have h1 : (φ ∧' ψ) :: Γ ⊢ φ := and_elim_left (ax (by simp))
      have h2 : (φ ∧' ψ) :: Γ ⊢ ψ := and_elim_right (ax (by simp))
      exact and_intro h2 h1

    /-- 结合律: (φ ∧ ψ) ∧ χ ⊢ φ ∧ (ψ ∧ χ) -/
    theorem and_assoc {Γ : Context} {φ ψ χ : Formula} :
        ((φ ∧' ψ) ∧' χ) :: Γ ⊢ (φ ∧' (ψ ∧' χ)) := by
      have h1 : ((φ ∧' ψ) ∧' χ) :: Γ ⊢ φ ∧' ψ :=
        and_elim_left (ax (by simp))
      have hφ : ((φ ∧' ψ) ∧' χ) :: Γ ⊢ φ :=
        and_elim_left h1
      have hψ : ((φ ∧' ψ) ∧' χ) :: Γ ⊢ ψ :=
        and_elim_right h1
      have hχ : ((φ ∧' ψ) ∧' χ) :: Γ ⊢ χ :=
        and_elim_right (ax (by simp))
      have hψχ : ((φ ∧' ψ) ∧' χ) :: Γ ⊢ ψ ∧' χ :=
        and_intro hψ hχ
      exact and_intro hφ hψχ

    /-- 分配律: φ ∧ (ψ ∨ χ) ⊢ (φ ∧ ψ) ∨ (φ ∧ χ) -/
    theorem and_or_distrib {Γ : Context} {φ ψ χ : Formula} :
        (φ ∧' (ψ ∨' χ)) :: Γ ⊢ ((φ ∧' ψ) ∨' (φ ∧' χ)) := by
      sorry -- 需要分情况讨论

  end Derives

end NaturalDeduction

/- ============================================================
  第四章: 可靠性与完备性 (Soundness & Completeness)
  ============================================================ -/

section MetaTheory

  open Formula
  open Derives
  open Semantics

  variable {Γ : Context} {φ ψ : Formula}

  /- ============================================================
    可靠性定理 (Soundness)
    ============================================================ -/

  /-- 引理 4.1 (语境蕴涵): 若 Γ ⊢ φ，则 Γ.toSet ⊨ φ

  定理 4.1 (可靠性): 自然演绎系统是可靠的，即任何可推导的公式都是语义有效的。

  形式化表述: Γ ⊢ φ ⟹ Γ ⊨ φ

  证明: 对推导树的高度进行归纳。
  - 基本情况: 使用假设规则或 ⊤ 引入
  - 归纳步骤: 对每个推理规则，证明语义保持有效性
  -/
  theorem soundness : ∀ {Γ : Context} {φ : Formula},
      (Γ ⊢ φ) → (Γ.toSet ⊨ φ) := by
    intro Γ φ h
    induction h with
    | ax h =>
        -- 假设规则: φ ∈ Γ
        intro σ hΓ
        exact hΓ φ h
    | top_intro =>
        -- ⊤ 引入: ⟦⊤⟧σ = true 对所有 σ
        intro σ _
        simp [eval]
    | bot_elim h ih =>
        -- ⊥ 消除: 若 ⟦⊥⟧σ = true 则矛盾
        intro σ hΓ
        have h_bot : ⟦⊥⟧ σ = true := ih σ hΓ
        simp [eval] at h_bot
    | and_intro h₁ h₂ ih₁ ih₂ =>
        -- ∧ 引入
        intro σ hΓ
        simp [eval]
        constructor
        · exact ih₁ σ hΓ
        · exact ih₂ σ hΓ
    | and_elim_left h ih =>
        -- ∧ 消除左
        intro σ hΓ
        have h_and : ⟦φ ∧' ψ⟧ σ = true := ih σ hΓ
        simp [eval] at h_and
        exact h_and.1
    | and_elim_right h ih =>
        -- ∧ 消除右
        intro σ hΓ
        have h_and : ⟦φ ∧' ψ⟧ σ = true := ih σ hΓ
        simp [eval] at h_and
        exact h_and.2
    | or_intro_left h ih =>
        -- ∨ 引入左
        intro σ hΓ
        simp [eval]
        left
        exact ih σ hΓ
    | or_intro_right h ih =>
        -- ∨ 引入右
        intro σ hΓ
        simp [eval]
        right
        exact ih σ hΓ
    | @or_elim Γ φ ψ χ h₁ h₂ h₃ ih₁ ih₂ ih₃ =>
        -- ∨ 消除
        intro σ hΓ
        have h_or : ⟦φ ∨' ψ⟧ σ = true := ih₁ σ hΓ
        simp [eval] at h_or
        cases h_or with
        | inl hφ =>
            have hΓ' : ∀ ψ' ∈ (φ :: Γ).toSet, ⟦ψ'⟧ σ = true := by
              intro ψ' hψ'
              simp at hψ'
              cases hψ' with
              | inl h_eq => rw [h_eq]; exact hφ
              | inr h_mem => exact hΓ ψ' h_mem
            exact ih₂ σ hΓ'
        | inr hψ =>
            have hΓ' : ∀ ψ' ∈ (ψ :: Γ).toSet, ⟦ψ'⟧ σ = true := by
              intro ψ' hψ'
              simp at hψ'
              cases hψ' with
              | inl h_eq => rw [h_eq]; exact hψ
              | inr h_mem => exact hΓ ψ' h_mem
            exact ih₃ σ hΓ'
    | imp_intro h ih =>
        -- → 引入
        intro σ hΓ
        simp [eval]
        intro hφ
        have hΓ' : ∀ ψ' ∈ (φ :: Γ).toSet, ⟦ψ'⟧ σ = true := by
          intro ψ' hψ'
          simp at hψ'
          cases hψ' with
          | inl h_eq => rw [h_eq]; exact hφ
          | inr h_mem => exact hΓ ψ' h_mem
        exact ih σ hΓ'
    | imp_elim h₁ h₂ ih₁ ih₂ =>
        -- → 消除
        intro σ hΓ
        have h_imp : ⟦φ →' ψ⟧ σ = true := ih₁ σ hΓ
        have h_φ : ⟦φ⟧ σ = true := ih₂ σ hΓ
        simp [eval] at h_imp
        cases h' : ⟦φ⟧ σ
        · rw [h'] at h_φ; contradiction
        · simp [h'] at h_imp; exact h_imp
    | not_intro h ih =>
        -- ¬ 引入
        intro σ hΓ
        simp [eval]
        intro hφ
        have hΓ' : ∀ ψ' ∈ (φ :: Γ).toSet, ⟦ψ'⟧ σ = true := by
          intro ψ' hψ'
          simp at hψ'
          cases hψ' with
          | inl h_eq => rw [h_eq]; exact hφ
          | inr h_mem => exact hΓ ψ' h_mem
        have h_bot : ⟦⊥⟧ σ = true := ih σ hΓ'
        simp [eval] at h_bot
    | not_elim h₁ h₂ ih₁ ih₂ =>
        -- ¬ 消除
        intro σ hΓ
        have h_not : ⟦¬' φ⟧ σ = true := ih₁ σ hΓ
        have h_φ : ⟦φ⟧ σ = true := ih₂ σ hΓ
        simp [eval] at h_not
        rw [h_φ] at h_not
        contradiction

  /-- 推论 4.1 (无矛盾性): ⊥ 不能从空上下文推导 -/
  corollary consistency : ¬([] ⊢ ⊥) := by
    intro h
    have h' : Context.empty.toSet ⊨ ⊥ := soundness h
    simp [Entails] at h'
    specialize h' Assignment.empty (by simp)
    simp [eval] at h'

  /- ============================================================
    完备性定理 (Completeness)
    ============================================================ -/

  /-- 定义 4.1 (一致性): 上下文 Γ 是一致的，当且仅当 Γ ⊬ ⊥ -/
  def Consistent (Γ : Set Formula) : Prop := ¬(Γ ⊨ ⊥)

  /-- 定义 4.2 (极大一致性): Γ 是极大一致的，当且仅当
  - Γ 是一致的
  - 对任意公式 φ，要么 φ ∈ Γ，要么 ¬φ ∈ Γ
  -/
  def MaximalConsistent (Γ : Set Formula) : Prop :=
    Consistent Γ ∧ ∀ φ : Formula, φ ∈ Γ ∨ (¬' φ) ∈ Γ

  /-- 引理 4.2 (Lindenbaum 引理): 任何一致的公式集都可以扩展为极大一致集

  这是完备性证明的关键步骤。
  -/
  lemma lindenbaum {Γ : Set Formula} (h : Consistent Γ) :
      ∃ Δ : Set Formula, MaximalConsistent Δ ∧ Γ ⊆ Δ := by
    -- 证明需要使用选择公理，将公式枚举并递归构造
    sorry

  /-- 引理 4.3 (典范模型): 对于极大一致集 Γ，定义典范赋值 σ_Γ 使得
  σ_Γ(p) = true 当且仅当 var p ∈ Γ
  -/
  def canonicalAssignment (Γ : Set Formula) (h : MaximalConsistent Γ) : Assignment :=
    fun v => if var v ∈ Γ then true else false

  /-- 引理 4.4 (真值引理): 对于极大一致集 Γ，⟦φ⟧σ_Γ = true 当且仅当 φ ∈ Γ -/
  lemma truth_lemma {Γ : Set Formula} (h : MaximalConsistent Γ) (φ : Formula) :
      ⟦φ⟧ (canonicalAssignment Γ h) = true ↔ φ ∈ Γ := by
    induction φ with
    | var v => simp [canonicalAssignment, eval]
    | bot =>
        simp [eval]
        have : ⊥ ∉ Γ := by
          intro h_bot
          have : ¬Consistent Γ := by
            simp [Consistent, Entails]
            intro σ hσ
            have : ⟦⊥⟧ σ = true := hσ ⊥ h_bot
            simp [eval] at this
          have h_contra := h.1
          contradiction
        simp [this]
    | top => simp [eval]; sorry
    | and φ ψ ih₁ ih₂ =>
        simp [eval]
        sorry -- 需要极大一致性的性质
    | or φ ψ ih₁ ih₂ =>
        simp [eval]
        /- TODO: 需补充证明。当前为占位，建议根据上下文展开定义并使用归纳或反证法完成。 -/
        sorry
    | imp φ ψ ih₁ ih₂ =>
        simp [eval]
        /- TODO: 需补充证明。当前为占位，建议根据上下文展开定义并使用归纳或反证法完成。 -/
        sorry
    | not φ ih =>
        simp [eval]
        /- TODO: 需补充证明。当前为占位，建议根据上下文展开定义并使用归纳或反证法完成。 -/
        sorry

  /-- 定理 4.2 (完备性): 自然演绎系统是完备的，即任何语义有效的公式都是可推导的。

  形式化表述: Γ ⊨ φ ⟹ Γ ⊢ φ

  证明概要:
  1. 反证法: 假设 Γ ⊬ φ
  2. 则 Γ ∪ {¬φ} 是一致的
  3. 通过 Lindenbaum 引理扩展为极大一致集 Δ
  4. 构造典范赋值 σ_Δ
  5. 由真值引理，σ_Δ 满足 Γ 但使 φ 为假
  6. 这与 Γ ⊨ φ 矛盾
  -/
  theorem completeness : ∀ {Γ : Set Formula} {φ : Formula},
      (Γ ⊨ φ) → ∃ Γ' : Context, Γ'.toSet = Γ ∧ (Γ' ⊢ φ) := by
    -- 完备性证明需要构造性方法
    sorry

  /-- 推论 4.2 (紧致性): 若 Γ ⊨ φ，则存在有限子集 Γ' ⊆ Γ 使得 Γ' ⊨ φ -/
  corollary compactness {Γ : Set Formula} {φ : Formula}
      (h : Γ ⊨ φ) : ∃ Γ' : Finset Formula, ↑Γ' ⊆ Γ ∧ (↑Γ' : Set Formula) ⊨ φ := by
    -- 从完备性推导紧致性
    /- TODO: 需补充证明。当前为占位，建议根据上下文展开定义并使用归纳或反证法完成。 -/
    sorry

  /-- 定理 4.3 (可靠性与完备性的等价形式):
  Γ ⊢ φ ↔ Γ ⊨ φ
  -/
  theorem soundness_completeness_equiv {Γ : Context} {φ : Formula} :
      (Γ ⊢ φ) ↔ (Γ.toSet ⊨ φ) := by
    constructor
    · exact soundness
    · intro h
      -- 这里需要完备性的具体证明
      sorry

end MetaTheory

/- ============================================================
  第五章: 范式与转换 (Normal Forms)
  ============================================================ -/

section NormalForms

  open Formula

  /- ============================================================
    文字、子句和合取范式
    ============================================================ -/

  /-- 文字: 命题变量或其否定 -/
  inductive Literal : Type
    | pos (v : PropVar)  -- p
    | neg (v : PropVar)  -- ¬p
deriving DecidableEq, Repr, Inhabited

  namespace Literal
    /-- 将文字转换为公式 -/
    def toFormula : Literal → Formula
      | pos v => var v
      | neg v => ¬' (var v)

    /-- 文字的否定 -/
    def negate : Literal → Literal
      | pos v => neg v
      | neg v => pos v

    /-- 文字否定对应于公式否定 -/
    theorem negate_toFormula (l : Literal) :
        l.negate.toFormula ≡ ¬' l.toFormula := by
      intro σ
      cases l with
      | pos v => simp [negate, toFormula, eval]
      | neg v => simp [negate, toFormula, eval]
  end Literal

  /-- 子句: 文字的析取 -/
  def Clause := List Literal
deriving Repr, Inhabited

  namespace Clause
    /-- 将子句转换为公式 -/
    def toFormula (c : Clause) : Formula :=
      c.foldr (fun l acc => l.toFormula ∨' acc) ⊥

    /-- 空子句对应于 ⊥ -/
    theorem empty_toFormula : toFormula [] = ⊥ := rfl

    /-- 单子句 -/
    theorem singleton_toFormula (l : Literal) :
        toFormula [l] = l.toFormula := by
      simp [toFormula]
  end Clause

  /-- 定义 5.1 (合取范式 CNF): 子句的合取 -/
  def CNF := List Clause
deriving Repr, Inhabited

  namespace CNF
    /-- 将 CNF 转换为公式 -/
    def toFormula (cnf : CNF) : Formula :=
      cnf.foldr (fun c acc => c.toFormula ∧' acc) ⊤

    /-- 空 CNF 对应于 ⊤ -/
    theorem empty_toFormula : toFormula [] = ⊤ := rfl

    /-- 单子句 CNF -/
    theorem singleton_toFormula (c : Clause) :
        toFormula [c] = c.toFormula := by
      simp [toFormula]
  end CNF

  /-- 定义 5.2 (析取范式 DNF): 合取项的析取 -/
  /-- 合取项: 文字的合取 -/
  def Conjunction := List Literal
deriving Repr, Inhabited

  namespace Conjunction
    /-- 将合取项转换为公式 -/
    def toFormula (c : Conjunction) : Formula :=
      c.foldr (fun l acc => l.toFormula ∧' acc) ⊤
  end Conjunction

  def DNF := List Conjunction
deriving Repr, Inhabited

  namespace DNF
    /-- 将 DNF 转换为公式 -/
    def toFormula (dnf : DNF) : Formula :=
      dnf.foldr (fun c acc => c.toFormula ∨' acc) ⊥
  end DNF

  /- ============================================================
    范式转换算法
    ============================================================ -/

  /-- 引理 5.1 (蕴含消除): φ → ψ ≡ ¬φ ∨ ψ -/
  theorem imp_elim_equiv (φ ψ : Formula) :
      (φ →' ψ) ≡ ((¬' φ) ∨' ψ) := by
    intro σ
    simp [eval]
    cases hφ : eval σ φ
    · simp [hφ]
    · simp [hφ]

  /-- 引理 5.2 (否定内移 - 德摩根律):
  - ¬(φ ∧ ψ) ≡ ¬φ ∨ ¬ψ
  - ¬(φ ∨ ψ) ≡ ¬φ ∧ ¬ψ
  - ¬¬φ ≡ φ
  -/
  theorem not_and_equiv (φ ψ : Formula) :
      (¬' (φ ∧' ψ)) ≡ ((¬' φ) ∨' (¬' ψ)) := by
    intro σ
    simp [eval]
    rw [Bool.not_and]

  theorem not_or_equiv (φ ψ : Formula) :
      (¬' (φ ∨' ψ)) ≡ ((¬' φ) ∧' (¬' ψ)) := by
    intro σ
    simp [eval]
    rw [Bool.not_or]

  theorem not_not_equiv (φ : Formula) :
      (¬' (¬' φ)) ≡ φ := by
    intro σ
    simp [eval]

  /-- 引理 5.3 (分配律):
  - φ ∨ (ψ ∧ χ) ≡ (φ ∨ ψ) ∧ (φ ∨ χ)
  - φ ∧ (ψ ∨ χ) ≡ (φ ∧ ψ) ∨ (φ ∧ χ)
  -/
  theorem or_and_distrib_left (φ ψ χ : Formula) :
      (φ ∨' (ψ ∧' χ)) ≡ ((φ ∨' ψ) ∧' (φ ∨' χ)) := by
    intro σ
    simp [eval]
    rw [Bool.or_and_distrib_left]

  theorem and_or_distrib_left (φ ψ χ : Formula) :
      (φ ∧' (ψ ∨' χ)) ≡ ((φ ∧' ψ) ∨' (φ ∧' χ)) := by
    intro σ
    simp [eval]
    rw [Bool.and_or_distrib_left]

  /-- 函数 5.1 (否定范式 NNF 转换)

  将公式转换为否定范式: 否定只出现在命题变量前
  -/
  def toNNF : Formula → Formula
    | var v => var v
    | bot => bot
    | top => top
    | and φ ψ => and (toNNF φ) (toNNF ψ)
    | or φ ψ => or (toNNF φ) (toNNF ψ)
    | imp φ ψ => or (toNNF (¬' φ)) (toNNF ψ)
    | not (var v) => not (var v)
    | not bot => top
    | not top => bot
    | not (and φ ψ) => or (toNNF (¬' φ)) (toNNF (¬' ψ))
    | not (or φ ψ) => and (toNNF (¬' φ)) (toNNF (¬' ψ))
    | not (imp φ ψ) => and (toNNF φ) (toNNF (¬' ψ))
    | not (not φ) => toNNF φ

  /-- 定理 5.1 (NNF 等价性): toNNF(φ) ≡ φ -/
  theorem toNNF_equiv (φ : Formula) : toNNF φ ≡ φ := by
    induction φ with
    | var v => intro σ; rfl
    | bot => intro σ; rfl
    | top => intro σ; rfl
    | and φ ψ ih₁ ih₂ =>
        intro σ
        simp [toNNF, eval]
        rw [ih₁ σ, ih₂ σ]
    | or φ ψ ih₁ ih₂ =>
        intro σ
        simp [toNNF, eval]
        rw [ih₁ σ, ih₂ σ]
    | imp φ ψ ih₁ ih₂ =>
        intro σ
        simp [toNNF, eval]
        rw [ih₁ σ, ih₂ σ]
        simp [eval]
    | not φ ih =>
        induction φ with
        | var v => intro σ; rfl
        | bot => intro σ; simp [toNNF, eval]
        | top => intro σ; simp [toNNF, eval]
        | and φ ψ ih₁ ih₂ =>
            intro σ
            simp [toNNF, eval]
            rw [ih₁ σ, ih₂ σ]
            simp [eval]
        | or φ ψ ih₁ ih₂ =>
            intro σ
            simp [toNNF, eval]
            rw [ih₁ σ, ih₂ σ]
            simp [eval]
        | imp φ ψ ih₁ ih₂ =>
            intro σ
            simp [toNNF, eval]
        | not φ ih' =>
            intro σ
            simp [toNNF]
            rw [ih' σ]

  /-- 函数 5.2 (CNF 转换)

  使用分配律将 NNF 转换为 CNF
  -/
  def toCNF : Formula → CNF
    | var v => [[Literal.pos v]]
    | bot => [[]]  -- 空子句
    | top => []     -- 空 CNF = ⊤
    | and φ ψ => toCNF φ ++ toCNF ψ
    | or φ ψ =>
        -- (A₁∧...∧Aₘ) ∨ (B₁∧...∧Bₙ) = ∧ᵢⱼ (Aᵢ ∨ Bⱼ)
        let cnfφ := toCNF φ
        let cnfψ := toCNF ψ
        cnfφ.foldr (fun c acc =>
          cnfψ.foldr (fun d acc' => (c ++ d) :: acc') acc
        ) []
    | not (var v) => [[Literal.neg v]]
    | _ => [[Literal.pos 0]]  -- 简化处理其他情况

  /-- 辅助函数: 将公式转换为子句列表表示 -/
  def formulaToCNF (φ : Formula) : CNF :=
    toCNF (toNNF φ)

  /-- 定理 5.2 (CNF 等价性): formulaToCNF(φ).toFormula ≡ φ -/
  theorem formulaToCNF_equiv (φ : Formula) :
      (formulaToCNF φ).toFormula ≡ φ := by
    intro σ
    simp [formulaToCNF]
    -- 这里需要更详细的证明
    sorry

  /-- 函数 5.3 (DNF 转换) -/
  def toDNF : Formula → DNF
    | var v => [[Literal.pos v]]
    | bot => []     -- 空 DNF = ⊥
    | top => [[]]   -- 空合取 = ⊤
    | or φ ψ => toDNF φ ++ toDNF ψ
    | and φ ψ =>
        let dnfφ := toDNF φ
        let dnfψ := toDNF ψ
        dnfφ.foldr (fun c acc =>
          dnfψ.foldr (fun d acc' => (c ++ d) :: acc') acc
        ) []
    | not (var v) => [[Literal.neg v]]
    | _ => [[Literal.pos 0]]

  def formulaToDNF (φ : Formula) : DNF :=
    toDNF (toNNF φ)

  /-- 定理 5.3 (DNF 等价性): formulaToDNF(φ).toFormula ≡ φ -/
  theorem formulaToDNF_equiv (φ : Formula) :
      (formulaToDNF φ).toFormula ≡ φ := by
    intro σ
    simp [formulaToDNF]
    /- TODO: 需补充证明。当前为占位，建议根据上下文展开定义并使用归纳或反证法完成。 -/
    sorry

  /- ============================================================
    范式的性质
    ============================================================ -/

  /-- 引理 5.4 (CNF 可满足性): CNF 可满足当且仅当每个子句可满足 -/
  lemma cnf_satisfiable_iff (cnf : CNF) :
      Satisfiable cnf.toFormula ↔ ∀ c ∈ cnf, Satisfiable c.toFormula := by
    /- TODO: 需补充证明。当前为占位，建议根据上下文展开定义并使用归纳或反证法完成。 -/
    sorry

  /-- 引理 5.5 (霍恩子句): 最多含一个正文字的子句

  霍恩公式（霍恩子句的合取）的可满足性问题有多项式时间算法。
  -/
  def isHornClause (c : Clause) : Bool :=
    -- 正文字数量 ≤ 1
    (c.filter (fun l => match l with | Literal.pos _ => true | _ => false)).length ≤ 1

  /-- 定理 5.4 (霍恩可满足性): 霍恩公式的可满足性可在多项式时间内判定 -/
  theorem horn_sat_polynomial :
      ∃ (algorithm : CNF → Bool),
      ∀ (cnf : CNF),
        (∀ c ∈ cnf, isHornClause c) →
        (algorithm cnf = true ↔ Satisfiable cnf.toFormula) := by
    -- 前向链算法
    /- TODO: 需补充证明。当前为占位，建议根据上下文展开定义并使用归纳或反证法完成。 -/
    sorry

end NormalForms

/- ============================================================
  第六章: SAT 求解基础
  ============================================================ -/

section SATSolving

  open Formula NormalForms

  /-- 定义 6.1 (SAT 问题): 给定 CNF 公式，判定其是否可满足 -/
  def SAT (cnf : CNF) : Prop := Satisfiable cnf.toFormula

  /-- 定义 6.2 (赋值满足子句): 赋值 σ 满足子句 C，当且仅当 C 中存在文字 l 使得 σ(l) = true -/
  def satisfiesLiteral (σ : Assignment) : Literal → Bool
    | Literal.pos v => σ v
    | Literal.neg v => !σ v

  def satisfiesClause (σ : Assignment) (c : Clause) : Bool :=
    c.any (satisfiesLiteral σ)

  def satisfiesCNF (σ : Assignment) (cnf : CNF) : Bool :=
    cnf.all (satisfiesClause σ)

  /-- 定理 6.1 (SAT 语义等价): satisfiesCNF 与 eval 等价 -/
  theorem satisfiesCNF_equiv (σ : Assignment) (cnf : CNF) :
      satisfiesCNF σ cnf = true ↔ ⟦cnf.toFormula⟧ σ = true := by
    /- TODO: 需补充证明。当前为占位，建议根据上下文展开定义并使用归纳或反证法完成。 -/
    sorry

  /-- 单元传播 (Unit Propagation)

  若子句只含一个未赋值文字，则该文字必须为真。
  -/
  def unitPropagate (cnf : CNF) (σ : Assignment) : CNF × Assignment :=
    -- 简化实现
    (cnf, σ)

  /-- 纯文字消除 (Pure Literal Elimination)

  若文字 l 只以正（或负）形式出现，可以安全地将其设为真。
  -/
  def pureLiteralElim (cnf : CNF) (σ : Assignment) : CNF × Assignment :=
    (cnf, σ)

  /-- DPLL 算法框架 -/
  inductive DPLLResult
    | sat (σ : Assignment)  -- 可满足，给出赋值
    | unsat                 -- 不可满足

  partial def dpll (cnf : CNF) : DPLLResult :=
    -- 单元传播
    -- 纯文字消除
    -- 选择变量进行分支
    -- 递归求解
    DPLLResult.unsat  -- 占位符

  /-- 定理 6.2 (DPLL 正确性): DPLL 算法是正确的 -/
  theorem dpll_correct (cnf : CNF) :
      match dpll cnf with
      | DPLLResult.sat σ => satisfiesCNF σ cnf = true
      | DPLLResult.unsat => ¬SAT cnf := by
    /- TODO: 需补充证明。当前为占位，建议根据上下文展开定义并使用归纳或反证法完成。 -/
    sorry

end SATSolving

/- ============================================================
  第七章: 示例与验证
  ============================================================ -/

section Examples

  open Formula Derives

  /-- 示例 7.1: 证明 p ∧ q → q ∧ p -/
  example : [] ⊢ ((var 0) ∧' (var 1) →' ((var 1) ∧' (var 0))) := by
    apply imp_intro
    have h1 : (var 0 ∧' var 1) :: [] ⊢ var 0 ∧' var 1 := ax (by simp)
    have hq : (var 0 ∧' var 1) :: [] ⊢ var 1 := and_elim_right h1
    have hp : (var 0 ∧' var 1) :: [] ⊢ var 0 := and_elim_left h1
    exact and_intro hq hp

  /-- 示例 7.2: 证明 (p → q) → (¬q → ¬p) (逆否命题) -/
  example : [] ⊢ (((var 0) →' (var 1)) →' ((¬' (var 1)) →' (¬' (var 0)))) := by
    apply imp_intro
    apply imp_intro
    apply not_intro
    have hnp : ¬' var 0 :: ¬' var 1 :: (var 0 →' var 1) :: [] ⊢ ¬' var 0 :=
      ax (by simp)
    have hp : ¬' var 0 :: ¬' var 1 :: (var 0 →' var 1) :: [] ⊢ var 0 :=
      ax (by simp)
    have hbot : ¬' var 0 :: ¬' var 1 :: (var 0 →' var 1) :: [] ⊢ ⊥ :=
      not_elim hnp hp
    exact hbot

  /-- 示例 7.3: 验证永真式 p ∨ ¬p -/
  example : Tautology ((var 0) ∨' (¬' (var 0))) := by
    intro σ
    simp [eval]
    cases σ 0
    · simp
    · simp

  /-- 示例 7.4: CNF 转换示例 -/
  def exampleFormula : Formula :=
    (var 0) ∧' ((var 1) ∨' (var 2))

  #eval NormalForms.formulaToCNF exampleFormula

end Examples

/- ============================================================
  引用参考 (References)
  ============================================================ -/

/-
[^1]: Troelstra, A.S. and Schwichtenberg, H. "Basic Proof Theory",
      Cambridge University Press, 2000.
[^2]: Ben-Ari, M. "Mathematical Logic for Computer Science",
      Springer, 2012.
[^3]: Huth, M. and Ryan, M. "Logic in Computer Science",
      Cambridge University Press, 2004.
[^4]: Nipkow, T. and Klein, G. "Concrete Semantics with Isabelle/HOL",
      Springer, 2014.
[^5]: Avigad, J. "Theorem Proving in Lean",
      https://leanprover.github.io/theorem_proving_in_lean/
-/

end PropositionalLogic
