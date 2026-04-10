/-
TypeSystem.lean - 类型系统主模块

本模块重新导出类型系统的所有子模块：
- SimpleTypes: 简单类型 λ→ 系统
- Safety: 类型安全定理

作者: AnalysisDataFlow Project
日期: 2026-04-10
-/

import FormalMethods.TypeSystem.SimpleTypes
import FormalMethods.TypeSystem.Safety

namespace FormalMethods.TypeSystem

-- 类型系统的基本概念重新导出
export SimpleTypes (Type TyArrow TyBool TyNat)
export SimpleTypes (Context emptyContext extendContext lookupContext)
export SimpleTypes (hasType)

end FormalMethods.TypeSystem
