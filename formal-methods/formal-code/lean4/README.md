# FormalMethods - Lean 4 形式化方法项目

本项目使用 Lean 4 对形式化方法的核心概念进行形式化验证，包括 Lambda 演算、类型系统、逻辑基础和并发理论。

## 项目结构

```
formal-code/lean4/
├── lakefile.toml              # Lake 项目配置
├── lean-toolchain             # Lean 版本指定 (v4.8.0)
├── Main.lean                  # 入口文件
├── README.md                  # 项目说明
├── FormalMethods.lean         # 主模块
└── FormalMethods/
    ├── Lambda.lean            # Lambda 演算主模块
    ├── Lambda/
    │   ├── Syntax.lean        # 语法定义
    │   ├── Substitution.lean  # 替换操作
    │   └── Reduction.lean     # 归约规则
    ├── TypeSystem.lean        # 类型系统主模块
    ├── TypeSystem/
    │   ├── SimpleTypes.lean   # 简单类型
    │   └── Safety.lean        # 类型安全
    ├── Logic.lean             # 逻辑基础
    └── Concurrent.lean        # 并发理论
```

## 构建指令

### 安装依赖

```bash
lake update
```

### 构建项目

```bash
lake build
```

### 运行示例

```bash
lake exe formalmethods
```

### 清理构建

```bash
lake clean
```

## 模块说明

### Lambda 演算 (Lambda/)

- **Syntax.lean**: 定义 Lambda 项的归纳类型，包括变量、抽象和应用
- **Substitution.lean**: 定义替换操作 [x := s]t 和 alpha 等价
- **Reduction.lean**: 定义 beta 归约和多步闭包

### 类型系统 (TypeSystem/)

- **SimpleTypes.lean**: 简单类型 λ→ 系统的语法和类型判断
- **Safety.lean**: 类型安全定理（保持性和进度性）的形式化证明

### 其他模块

- **Logic.lean**: 命题逻辑和谓词逻辑的形式化
- **Concurrent.lean**: 并发计算模型（CSP/CCS）的形式化

## 核心概念

### Lambda 演算语法

```
t ::= x       -- 变量 (Var)
    | λx.t    -- 抽象 (Abs)
    | t t     -- 应用 (App)
```

### Beta 归约

```
(λx.t) s →β [x := s]t
```

### 类型安全

- **保持性 (Preservation)**: 如果 `⊢ t : T` 且 `t → t'`，则 `⊢ t' : T`
- **进度性 (Progress)**: 如果 `⊢ t : T`，则 `t` 是值或存在 `t'` 使得 `t → t'`

## 定理列表

### Lambda 演算

| 定理 | 描述 | 文件 |
|------|------|------|
| `subst_fv` | 替换保持自由变量集合 | Substitution.lean |
| `alpha_equiv_refl` | α 等价的自反性 | Substitution.lean |
| `beta_deterministic` | β 归约的确定性 | Reduction.lean |

### 类型安全

| 定理 | 描述 | 文件 |
|------|------|------|
| `preservation` | 类型保持性 | Safety.lean |
| `progress` | 进度性 | Safety.lean |
| `type_safety` | 类型安全定理 | Safety.lean |

## 参考文献

1. Pierce, B. C. (2002). *Types and Programming Languages*. MIT Press.
2. Nipkow, T., & Klein, G. (2014). *Concrete Semantics*. Springer.
3. Avigad, J., et al. (2021). *Theorem Proving in Lean 4*.
4. Moura, L., & Ullrich, S. (2021). The Lean 4 Theorem Prover.

## 许可证

本项目作为 AnalysisDataFlow 项目的一部分，遵循相同的使用条款。
