/-
Syntax.lean - Lambda 演算语法定义

本文件定义了无类型 Lambda 演算 (Untyped Lambda Calculus) 的语法。

语法定义:
  t ::= x           -- 变量 (Variable)
      | λx. t       -- 抽象 (Abstraction)
      | t t         -- 应用 (Application)

作者: AnalysisDataFlow Project
日期: 2026-04-10
-/

namespace FormalMethods.Lambda.Syntax

/-- 
变量名使用字符串表示
使用 String 而不是 Nat 是为了可读性，
实际证明中可以通过 de Bruijn 索引转换为 Nat
-/
abbrev Name := String

/-- 
项 (Term) 的归纳定义

这是无类型 Lambda 演算的核心语法。
-/
inductive Term : Type where
  | var : Name → Term           -- 变量 x
  | abs : Name → Term → Term    -- 抽象 λx. t
  | app : Term → Term → Term    -- 应用 t s
  deriving Repr, BEq, Inhabited

-- 打开 Term 命名空间以使用构造器
open Term

/-! 
## 记号 (Notation)

定义一些方便的记号，使得 Lambda 项更易读。
-/

/-- 变量构造 -/
def mkVar (x : Name) : Term := var x

/-- 抽象构造: λx. t -/
def mkAbs (x : Name) (t : Term) : Term := abs x t

/-- 应用构造: t s -/
def mkApp (t s : Term) : Term := app t s

/-! 
## 示例项

定义一些经典的 Lambda 演算项作为示例。
-/

/-- 恒等函数: I = λx. x -/
def identity : Term :=
  abs "x" (var "x")

/-- 自应用: ω = λx. x x -/
def omegaTerm : Term :=
  abs "x" (app (var "x") (var "x"))

/-- Omega 组合子: Ω = ω ω -/
def Omega : Term :=
  app omegaTerm omegaTerm

/-- 邱奇数 0: λf. λx. x -/
def churchZero : Term :=
  abs "f" (abs "x" (var "x"))

/-- 邱奇数 1: λf. λx. f x -/
def churchOne : Term :=
  abs "f" (abs "x" (app (var "f") (var "x")))

/-- 邱奇数 2: λf. λx. f (f x) -/
def churchTwo : Term :=
  abs "f" (abs "x" (app (var "f") (app (var "f") (var "x"))))

/-! 
## 自由变量 (Free Variables)

自由变量是指在项中不被任何 λ 抽象绑定的变量。
-/

/-- 
自由变量集合
返回给定项中所有自由变量的集合。
-/
def fv : Term → List Name
  | var x => [x]
  | abs x t => List.filter (fun y => y ≠ x) (fv t)
  | app t₁ t₂ => fv t₁ ++ fv t₂

/-- 
项的大小（节点数）

用于证明替换操作的终止性。
-/
def size : Term → Nat
  | var _ => 1
  | abs _ t => 1 + size t
  | app t₁ t₂ => 1 + size t₁ + size t₂

@[simp]
theorem size_pos (t : Term) : size t > 0 := by
  induction t with
  | var x => simp [size]
  | abs x t ih => simp [size]; linarith
  | app t₁ t₂ ih₁ ih₂ => simp [size]; linarith

/-- 
变量在项中是否自由
-/
def isFreeVar (x : Name) (t : Term) : Bool :=
  x ∈ fv t

/-- 
变量在项中是否被绑定
-/
def isBoundVar (x : Name) (t : Term) : Bool :=
  match t with
  | var _ => false
  | abs y body => x = y || isBoundVar x body
  | app t₁ t₂ => isBoundVar x t₁ || isBoundVar x t₂

/-! 
## 封闭项 (Closed Terms)

封闭项是指没有自由变量的项，也称为组合子 (Combinator)。
-/

/-- 
判断项是否为封闭项
-/
def isClosed (t : Term) : Bool :=
  fv t == []

/-- 
封闭项的类型定义
-/
def ClosedTerm := { t : Term // isClosed t }

/-! 
## 变量新鲜性 (Freshness)

用于生成在项中未使用的新变量名。
-/

/-- 
生成新鲜变量名

给定一个变量名前缀和一个项，生成一个不在该项中的新变量名。
使用简单的策略：添加数字后缀直到找到未使用的名字。
-/
def freshVar (base : Name) (t : Term) : Name :=
  base ++ "_" ++ (List.length (fv t)).repr

/-! 
## 辅助引理

关于语法的基本性质。
-/

-- 变量的自由变量就是其本身
@[simp]
theorem fv_var (x : Name) : fv (var x) = [x] := by
  simp [fv]

-- 抽象的自由变量是体中自由变量去掉绑定变量
@[simp]
theorem fv_abs (x : Name) (t : Term) : 
  fv (abs x t) = List.filter (fun y => y ≠ x) (fv t) := by
  simp [fv]

-- 应用的自由变量是两个子项自由变量的并
@[simp]
theorem fv_app (t₁ t₂ : Term) : 
  fv (app t₁ t₂) = fv t₁ ++ fv t₂ := by
  simp [fv]

-- 恒等函数是封闭项
theorem identity_closed : isClosed identity := by
  simp [isClosed, identity]

-- Omega 组合子是封闭项（用于证明停机性相关性质）
theorem omega_closed : isClosed Omega := by
  simp [isClosed, Omega, omegaTerm]

end FormalMethods.Lambda.Syntax
