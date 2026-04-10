/-
Lambda.lean - Lambda 演算主模块

本模块重新导出 Lambda 演算的所有子模块：
- Syntax: 语法定义
- Substitution: 替换操作
- Reduction: 归约规则

提供统一的 Lambda 演算接口。

作者: AnalysisDataFlow Project
日期: 2026-04-10
-/

import FormalMethods.Lambda.Syntax
import FormalMethods.Lambda.Substitution
import FormalMethods.Lambda.Reduction

-- 公开所有子模块的命名空间
namespace FormalMethods.Lambda

-- 可选：在此定义一些常用的组合子

/-- 恒等函数: I = λx. x -/
def I : Term :=
  Term.abs "x" (Term.var "x")

/-- 布尔值真: true = λt. λf. t -/
def tru : Term :=
  Term.abs "t" (Term.abs "f" (Term.var "t"))

/-- 布尔值假: false = λt. λf. f -/
def fls : Term :=
  Term.abs "t" (Term.abs "f" (Term.var "f"))

/-- 条件表达式: if = λb. λt. λf. b t f -/
def cond : Term :=
  Term.abs "b" (Term.abs "t" (Term.abs "f" 
    (Term.app (Term.app (Term.var "b") (Term.var "t")) (Term.var "f"))))

end FormalMethods.Lambda
