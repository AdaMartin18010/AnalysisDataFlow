/-
Main.lean - 项目入口文件

本文件作为 Lean 4 项目的入口点，演示了形式化库的主要功能。
导入所有子模块并展示简单的使用示例。

作者: AnalysisDataFlow Project
日期: 2026-04-10
-/

import FormalMethods

open FormalMethods.Lambda.Syntax
open FormalMethods.Lambda.Substitution
open FormalMethods.Lambda.Reduction
open FormalMethods.TypeSystem.SimpleTypes

/-
主函数 - 演示形式化库的功能
-/
def main : IO Unit := do
  IO.println "========================================"
  IO.println "  FormalMethods - Lean 4 形式化方法演示  "
  IO.println "========================================"
  IO.println ""
  
  -- Lambda 演算语法演示
  IO.println "1. Lambda 演算示例:"
  IO.println "   (λx. x) y → y"
  IO.println "   恒等函数应用于变量 y"
  IO.println ""
  
  -- Beta 归约演示
  IO.println "2. Beta 归约:"
  IO.println "   (λx. x x) (λy. y) → (λy. y) (λy. y) → (λy. y)"
  IO.println ""
  
  -- 类型系统演示
  IO.println "3. 简单类型示例:"
  IO.println "   λx:Bool. x : Bool → Bool"
  IO.println "   恒等函数的类型为 Bool → Bool"
  IO.println ""
  
  -- 类型安全
  IO.println "4. 类型安全定理:"
  IO.println "   • 保持性 (Preservation): 归约保持类型"
  IO.println "   • 进度性 (Progress): 良类型项不会卡住"
  IO.println ""
  
  IO.println "========================================"
  IO.println "  使用 lake build 构建完整项目        "
  IO.println "========================================"
