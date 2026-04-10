/-
FormalMethods.lean - 主模块文件

这是 FormalMethods 库的主入口模块，重新导出所有子模块，
使得用户可以通过 `import FormalMethods` 一次性导入整个库。

模块依赖关系:
- Lambda
  - Syntax ← Substitution ← Reduction
- TypeSystem
  - SimpleTypes ← Safety
- Logic
- Concurrent

作者: AnalysisDataFlow Project
日期: 2026-04-10
-/

-- Lambda 演算相关模块
import FormalMethods.Lambda.Syntax
import FormalMethods.Lambda.Substitution
import FormalMethods.Lambda.Reduction

-- 类型系统相关模块
import FormalMethods.TypeSystem.SimpleTypes
import FormalMethods.TypeSystem.Safety

-- 其他形式化模块
import FormalMethods.Logic
import FormalMethods.Concurrent
