/-
Substitution.lean - Lambda 演算替换操作

本文件定义 Lambda 演算中的替换操作 [x := s]t，
即将项 t 中变量 x 的所有自由出现替换为项 s。

主要定义:
- 替换操作 subst x s t = [x := s]t
- 避免变量捕获的机制
- Alpha 等价 (α-equivalence)

作者: AnalysisDataFlow Project
日期: 2026-04-10
-/

import FormalMethods.Lambda.Syntax

namespace FormalMethods.Lambda.Substitution

open Syntax.Term
open Syntax

/-! 
## 替换操作

替换 [x := s]t 的定义需要注意避免变量捕获 (variable capture)。
-/

/-- 
替换操作

将项 t 中变量 x 的所有自由出现替换为项 s。
使用简单的方法：如果会发生变量捕获，先重命名绑定变量。

定义:
  [x := s]x = s
  [x := s]y = y        (if y ≠ x)
  [x := s](λy. t) = λy. [x := s]t  (if y ≠ x and y ∉ fv(s))
  [x := s](t₁ t₂) = ([x := s]t₁) ([x := s]t₂)
-/
def subst (x : Name) (s t : Term) : Term :=
  match t with
  | var y =>
      if y = x then s else var y
  | abs y body =>
      if y = x then
        -- x 被绑定，不替换
        abs y body
      else if y ∈ fv s then
        -- 避免变量捕获：重命名 y 为新鲜变量
        let y' := freshVar y (app s body)
        abs y' (subst x s (subst y (var y') body))
      else
        -- 安全替换
        abs y (subst x s body)
  | app t₁ t₂ =>
      app (subst x s t₁) (subst x s t₂)

/-- 
替换操作的记号表示
-/
notation:80 "[" x ":=" s "]" t => subst x s t

/-! 
## 替换的基本性质
-/

/-- 
替换不影响非目标变量

如果 x ≠ y，则 [x := s]y = y
-/
lemma subst_var_neq {x y : Name} {s : Term} (h : x ≠ y) : 
  [x := s] (var y) = var y := by
  simp [subst, h]

/-- 
替换目标变量

[x := s]x = s
-/
lemma subst_var_eq (x : Name) (s : Term) : 
  [x := s] (var x) = s := by
  simp [subst]

/-- 
替换不改变自由变量集合（除非替换变量本身）

如果 x ∉ fv(t)，则 fv([x := s]t) = fv(t)
-/
lemma subst_fv_notin {x : Name} {s t : Term} (h : x ∉ fv t) : 
  fv ([x := s] t) = fv t := by
  induction t with
  | var y =>
      simp [subst]
      split_ifs with h1
      · -- y = x, 但 x ∉ fv(var y) = {y}，矛盾
        exfalso
        simp_all [fv]
      · -- y ≠ x，无变化
        simp [fv]
  | abs y body ih =>
      simp [fv, h] at *
      split_ifs with h1 h2
      · -- y = x
        simp [fv, h1]
      · -- y ≠ x but y ∈ fv(s)，重命名情况
        simp [fv, ih]
        /- 证明: [x:=s](λy.t) = λz. [x:=s]([y:=z]t)，其中 z 是新鲜变量。
           需证: fv(λz. [x:=s]([y:=z]t)) = (fv(λy.t) \ {x}) ∪ fv(s)
           左边 = fv([x:=s]([y:=z]t)) \ {z}
           由 IH 于 [y:=z]t: = (fv([y:=z]t) \ {x}) ∪ fv(s) \ {z}
           fv([y:=z]t) = (fv(t) \ {y}) ∪ {z}（因 z 新鲜）
           故 = ((fv(t) \ {y}) ∪ {z} \ {x}) ∪ fv(s) \ {z}
           由于 z ∉ fv(s)（新鲜性），z ∉ fv(t) \ {y}（若 z 足够新鲜），
           且 z ≠ x（若选择得当），可简化为 (fv(t) \ {y, x}) ∪ fv(s)
           右边 = (fv(t) \ {y, x}) ∪ fv(s)（因 y ≠ x）
           两边相等。
        -/
        -- [FORMAL-GAP-N-02] 需建立 fv 在重命名替换下的精确等式：
        --   fv([y:=z]t) = (fv(t) \ {y}) ∪ {z}
        -- 此性质依赖 freshVar 的正确性和 fv 的归纳定义。
        -- 完成后可用 set 推理（tauto / omega）消去。
        sorry
      · -- y ≠ x and y ∉ fv(s)
        simp [fv, ih]
  | app t₁ t₂ ih₁ ih₂ =>
      simp [fv] at h ⊢
      simp [ih₁, ih₂]
      all_goals tauto

/-- 
替换后自由变量的变化

fv([x := s]t) ⊆ (fv(t) \ {x}) ∪ fv(s)
-/
lemma subst_fv_subset {x : Name} {s t : Term} : 
  fv ([x := s] t) ⊆ (fv t).erase x ++ fv s := by
  induction t with
  | var y =>
      simp [subst]
      split_ifs with h
      · -- y = x
        simp [h]
      · -- y ≠ x
        simp
  | abs y body ih =>
      simp [subst]
      split_ifs with h1 h2
      · -- y = x
        simp [fv, h1]
      · -- y ≠ x, y ∈ fv(s)
        simp [fv]
        /- 证明: [x:=s](λy.t) = λz. [x:=s]([y:=z]t)，其中 z 新鲜。
           需证: fv(λz. [x:=s]([y:=z]t)) ⊆ (fv(λy.t) \ {x}) ∪ fv(s)
           左边 = fv([x:=s]([y:=z]t)) \ {z}
           由 IH: ⊆ ((fv([y:=z]t) \ {x}) ∪ fv(s)) \ {z}
           fv([y:=z]t) ⊆ (fv(t) \ {y}) ∪ {z}
           故 ⊆ (((fv(t) \ {y}) ∪ {z}) \ {x}) ∪ fv(s)) \ {z}
           由于 z 新鲜，z ∉ fv(s)，可简化为 (fv(t) \ {y, x}) ∪ fv(s)
           右边 = (fv(t) \ {y, x}) ∪ fv(s)（因 fv(λy.t) = fv(t) \ {y}）
           包含关系成立。
        -/
        -- [FORMAL-GAP-N-03] 同上：fv 在重命名替换下的子集关系。
        --   fv([y:=z]t) ⊆ (fv(t) \ {y}) ∪ {z}
        -- 结合 IH 和 freshVar 性质可得。
        sorry
      · -- y ≠ x, y ∉ fv(s)
        simp [fv, ih]
  | app t₁ t₂ ih₁ ih₂ =>
      simp [fv, List.append_subset, ih₁, ih₂]

/-! 
## Alpha 等价 (α-equivalence)

Alpha 等价是指两个 Lambda 项仅通过重命名绑定变量而等价。
例如: λx. x =α λy. y
-/

/-- 
Alpha 等价的定义

两个项是 alpha 等价的，如果它们仅在绑定变量名上不同。
-/
inductive AlphaEquiv : Term → Term → Prop where
  | var (x : Name) : 
      AlphaEquiv (var x) (var x)
  
  | abs_same (x : Name) (t₁ t₂ : Term) : 
      AlphaEquiv t₁ t₂ → 
      AlphaEquiv (abs x t₁) (abs x t₂)
  
  | abs_rename (x y : Name) (t : Term) : 
      y ∉ fv t → 
      AlphaEquiv (abs x t) (abs y ([x := var y] t))
  
  | app (t₁ t₂ s₁ s₂ : Term) : 
      AlphaEquiv t₁ s₁ → 
      AlphaEquiv t₂ s₂ → 
      AlphaEquiv (app t₁ t₂) (app s₁ s₂)

/-- 
Alpha 等价的记号
-/
infix:50 " =α " => AlphaEquiv

/-! 
## Alpha 等价的性质
-/

/-- 
Alpha 等价是自反的
-/
lemma alpha_equiv_refl (t : Term) : t =α t := by
  induction t with
  | var x => 
      apply AlphaEquiv.var
  | abs x body ih => 
      apply AlphaEquiv.abs_same
      exact ih
  | app t₁ t₂ ih₁ ih₂ => 
      apply AlphaEquiv.app
      · exact ih₁
      · exact ih₂

/-- 
Alpha 等价是对称的
-/
lemma alpha_equiv_symm {t s : Term} (h : t =α s) : s =α t := by
  induction h with
  | var x => 
      apply AlphaEquiv.var
  | abs_same x t₁ t₂ _ ih => 
      apply AlphaEquiv.abs_same
      exact ih
  | abs_rename x y t h_fresh => 
      /- 证明: 若 abs x t =α abs y ([x:=var y]t)，则反向也成立。
         即 abs y ([x:=var y]t) =α abs x t。
         应用 abs_rename 规则: 需找 z 使
         abs y ([x:=var y]t) =α abs z ([y:=var z]([x:=var y]t))
         取 z = x（若 x 不在 [x:=var y]t 的自由变量中，即 x ∉ fv([x:=var y]t)）。
         由替换性质: x ∉ fv([x:=var y]t) 成立（因为 x 被替换掉了）。
         故 abs y ([x:=var y]t) =α abs x ([y:=var x]([x:=var y]t))
         需证 [y:=var x]([x:=var y]t) =α t。
         这是 "逆替换" 性质: 若 y 新鲜，则 [y:=x]([x:=y]t) =α t。
      -/
      -- [FORMAL-GAP-N-04] "逆替换"性质：若 y 新鲜，则 [y:=x]([x:=y]t) =α t。
      -- 这是 α-等价对称性的核心引理，证明需对 t 结构归纳，
      -- 在 abs 情形利用 freshVar 避免捕获。
      sorry
  | app t₁ t₂ s₁ s₂ _ _ ih₁ ih₂ => 
      apply AlphaEquiv.app
      · exact ih₁
      · exact ih₂

/-! 
## 替换与 Alpha 等价的交互
-/

/-- 
替换保持 Alpha 等价

如果 t₁ =α t₂，则 [x := s]t₁ =α [x := s]t₂
-/
lemma subst_preserves_alpha {x : Name} {s t₁ t₂ : Term} 
    (h : t₁ =α t₂) : 
  [x := s] t₁ =α [x := s] t₂ := by
  /- 证明策略: 对 AlphaEquiv 关系进行结构归纳。
     
     Case var: t₁ = var z, t₂ = var z。
     [x:=s](var z) 两边相同，由 alpha_equiv_refl 得证。
     
     Case abs_same: t₁ = abs y t₁', t₂ = abs y t₂'，t₁' =α t₂'。
     由 IH: [x:=s]t₁' =α [x:=s]t₂'。
     若 y = x: [x:=s](λx.t₁') = λx.t₁' =α λx.t₂' = [x:=s](λx.t₂')
     若 y ≠ x 且 y ∈ fv(s): 两边都重命名为新鲜变量 z，
       由 IH 于 [y:=z]t₁' 和 [y:=z]t₂' 得证。
     若 y ≠ x 且 y ∉ fv(s): 直接由 abs_same 和 IH 得证。
     
     Case abs_rename: t₁ = abs y t, t₂ = abs z ([y:=var z]t)，z 新鲜。
     需证 [x:=s](λy.t) =α [x:=s](λz.[y:=var z]t)。
     分情况讨论 x 与 y, z 的关系，利用替换的交换性。
     
     Case app: 直接由 app 规则和两个 IH 得证。
  -/
  -- [FORMAL-GAP-N-05] 替换保持 α-等价。
  -- 证明策略: 对 AlphaEquiv 关系结构归纳。
  --   Case abs_same: 直接由 IH + abs_same / abs_rename。
  --   Case abs_rename: 需利用替换的交换性 [x:=s](λy.t) =α [x:=s](λz.[y:=z]t)。
  --     分 x=y, x=z, x∉{y,z} 三种情形，分别应用 subst 定义和 abs_rename。
  --   Case app: 直接由 IH + AlphaEquiv.app。
  -- 此引理完成後，Safety.lean 中 substitution_lemma 的 abs 分支可消去 sorry。
  sorry

end FormalMethods.Lambda.Substitution
