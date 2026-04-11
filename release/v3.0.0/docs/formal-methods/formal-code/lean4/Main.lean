/-
  # Main.lean - FormalMethods 项目入口

  此文件作为 Lean 4 项目的可执行入口点。
  导入所有形式化模块并提供基本的运行接口。

  ## 导入的模块

  - `FormalMethods.Lambda`: 简单类型 Lambda 演算
    - `Syntax`: 语法定义
    - `Operational`: 操作语义
    - `Typing`: 类型系统
    - `Safety`: 类型安全定理

  - `FormalMethods.TypeSystem`: 类型系统
    - `SystemF`: System F (多态 Lambda 演算)

  - `FormalMethods.Logic`: 逻辑
    - `Propositional`: 命题逻辑

  - `FormalMethods.Concurrent`: 并发
    - `CCS`: 通信系统演算
-/

import FormalMethods.Lambda.Syntax
import FormalMethods.Lambda.Operational
import FormalMethods.Lambda.Typing
import FormalMethods.Lambda.Safety
import FormalMethods.TypeSystem.SystemF
import FormalMethods.Logic.Propositional
import FormalMethods.Concurrent.CCS

/-
  主函数 - 作为可执行程序的入口点
  在 Lean 4 中，此函数可以通过 `lake exe formal_methods` 运行
-/.
def main : IO Unit := do
  IO.println "================================"
  IO.println "  FormalMethods - Lean 4 形式化项目"
  IO.println "================================"
  IO.println ""
  IO.println "本项目包含以下形式化内容："
  IO.println ""
  IO.println "1. Lambda 演算 (Simply Typed Lambda Calculus)"
  IO.println "   - 语法定义"
  IO.println "   - 操作语义"
  IO.println "   - 类型系统"
  IO.println "   - 类型安全定理 (Progress + Preservation)"
  IO.println ""
  IO.println "2. System F (多态 Lambda 演算)"
  IO.println ""
  IO.println "3. 命题逻辑"
  IO.println ""
  IO.println "4. CCS (通信系统演算)"
  IO.println ""
  IO.println "================================"
