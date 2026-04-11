# 逻辑形式化模块 (Logic Formalization)

本目录包含逻辑系统的 Lean 4 形式化实现。

## 文件结构

```
FormalMethods/Logic/
├── Propositional.lean    # 命题逻辑完整形式化 (独立命名空间)
├── Predicate.lean        # 谓词逻辑完整形式化 (L6级别)
├── HOL.lean             # 高阶逻辑(HOL)完整形式化 (L6级别)
├── Modal.lean           # 模态逻辑完整形式化 (L5级别)
└── README.md            # 本文件
```

## 命题逻辑 (Propositional.lean)

包含以下内容：

- 语法：命题变量、公式定义
- 语义：真值赋值、公式求值
- 语义概念：重言式、可满足性、逻辑蕴涵
- 自然演绎系统：完整的推导规则
- 元定理：可靠性定理、完备性定理框架
- 范式：CNF、DNF、NNF 转换

## 谓词逻辑 (Predicate.lean)

包含完整的一阶谓词逻辑形式化：

### 1. 签名 (Signature)

- 函数符号与谓词符号
- 元数函数 arity
- 等号支持

### 2. 语法 (Syntax)

- 项 (Term)：变量、函数应用
- 公式 (Formula)：原子公式、连接词、量词
- 自由变量计算

### 3. 替换 (Substitution)

- 替换定义 σ: Var → Term
- 单点替换 [t/x]
- 替换在项和公式上的应用
- 替换引理框架

### 4. 语义 (Semantics)

- 结构/模型 Structure
- 赋值 Assignment
- 项解释 interpTerm
- 公式满足关系 M ⊨ φ[ρ]
- 可满足性、有效性、逻辑后承

### 5. 自然演绎系统 (Natural Deduction)

完整规则集包括：

- **命题规则**：假设、⊤/⊥、∧、∨、→、¬
- **量词规则**：
  - ∀ 引入 (∀+)：需变量 freshness 条件
  - ∀ 消除 (∀-)
  - ∃ 引入 (∃+)
  - ∃ 消除 (∃-)：需新鲜变量条件
- **等式规则**：
  - 自反性 (refl)
  - 对称性 (symm)
  - 传递性 (trans)
  - 替换公理 (subst)

### 6. 元定理 (Meta-Theory)

- **可靠性定理** (Soundness)：Γ ⊢ φ → Γ ⊨ φ
- **完备性定理** (Completeness)：Γ ⊨ φ → Γ ⊢ φ
- **Lindenbaum 引理**：一致集可扩展为极大一致集
- **Henkin 构造**：完备性证明的关键
- **Löwenheim-Skolem 定理**：向下和向上版本
- **紧致性定理** (Compactness)
- **替换引理** (Substitution Lemma)

### 7. 应用示例

#### 群论 (Group Theory)

```lean
def GroupSig : Signature := ...
def GroupAxioms : List GFormula :=
  [assoc_axiom, left_id_axiom, right_id_axiom, left_inv_axiom, right_inv_axiom]
def IsGroup (M : Structure GroupSig) : Prop := ...
```

#### Peano 算术

```lean
def PASig : Signature := ...
def PAAxiomsBasic : List PAFormula := [S1, S2, S3, S4, S5, S6]
def StandardModel : Structure PASig := ...
```

## 使用方式

```lean
import FormalMethods.Logic.Predicate

open PredicateLogic

-- 定义简单签名
inductive MyFunc | f  -- 一元函数
inductive MyPred | P  -- 一元谓词

def MySig : Signature := ⟨MyFunc, MyPred,
  fun _ => 1, fun _ => 1, true⟩

-- 创建公式
abbrev F := Formula MySig String
example : F := ∀' "x", Formula.pred MyPred.P [Term.var "x"]
```

## 形式化等级

- **L5**: 严格形式化，包含完整证明结构
- **L6**: 完整形式化，包含复杂构造性证明

## 依赖关系

```
Predicate.lean
├── Mathlib.Data.Set.Basic
├── Mathlib.Data.Finset.Basic
├── Mathlib.Data.Nat.Basic
└── Mathlib.Tactic
```

## 高阶逻辑 (HOL.lean)

包含完整的高阶逻辑(HOL)形式化，是Isabelle/HOL、HOL4等定理证明器的理论基础：

### 1. 简单类型系统 (Simple Type Theory)

- 基本类型: Bool, Nat, Ind
- 函数类型: σ → τ
- 积类型: σ × τ
- 类型变量: α, β, γ
- 类型环境的弱化引理

### 2. HOL项和类型判断

- 项构造: 变量、常量、λ抽象、应用、对、投影
- 常量: 逻辑常量(⊤, ⊥, ¬, ∧, ∨, →, =, ∀, ∃)、选择算子(ε, ι)、算术常量
- 完整的类型判断系统
- 类型唯一性定理
- 弱化引理

### 3. 等式推理与转换

- 替换操作 (substitution)
- α-等价
- β-规约及其保持类型
- β-规约的自反传递闭包
- η-转换
- Church-Rosser性质
- 等式推理系统 (自反、对称、传递、同余)

### 4. 经典推理规则

- 排中律 (LEM): ∀φ. φ ∨ ¬φ
- 双重否定消除 (DNE)
- Hilbert选择算子 (ε)
- 描述算子 (ι)
- 无穷公理

### 5. 形式化数学基础

- Peano算术公理
- 自然数运算 (加法、乘法)
- 数学归纳法原理
- 良基归纳法
- 集合论基础 (集合作为谓词)
- Cantor定理

### 6. HOL证明系统

- 完整的推导规则
- 演绎定理
- 可靠性定理
- Henkin语义完备性

### 7. 元理论性质

- 强规范化
- 一致性 (相对于集合论)
- 表达能力分析

## 模态逻辑 (Modal.lean)

包含完整的模态逻辑形式化，包括Kripke语义、正规模态逻辑系统和时态逻辑扩展：

### 1. 模态逻辑语法

- **命题变量**: 自然数标识的原子命题
- **经典连接词**: ∧, ∨, →, ¬, ⊤, ⊥
- **模态算子**:
  - □ φ (必然): φ 在所有可达世界为真
  - ◇ φ (可能): φ 在某个可达世界为真
- **公式类型**: `ModalFormula` 归纳定义
- **□◇对偶性**: ◇φ ≡ ¬□¬φ, □φ ≡ ¬◇¬φ

### 2. Kripke语义

- **可能世界** (`World`): 命题变量到布尔值的映射
- **可达关系** (`Accessibility`): 世界间的二元关系
- **Kripke框架**: (W, R) - 世界集合加可达关系
- **估值函数** (`Valuation`): 命题变量到世界集合的映射
- **Kripke模型**: (W, R, V) - 框架加估值
- **满足关系** (⊨): 模型-世界-公式的三元关系
- **语义概念**: 有效性、可满足性、语义后承

### 3. 框架性质与对应

- **自反性** ↔ T公理 (□φ → φ)
- **传递性** ↔ 4公理 (□φ → □□φ)
- **对称性** ↔ B公理 (φ → □◇φ)
- **欧几里得性** ↔ 5公理 (◇φ → □◇φ)
- **串行性**: ∀w, ∃w'. R w w'

### 4. 正规模态逻辑系统

- **K系统**: 最基本的正规模态逻辑
  - K公理: □(φ→ψ) → (□φ→□ψ) (分配公理)
  - 必然化规则: ⊢φ ⟹ ⊢□φ
- **T系统**: K + T公理
  - 对应自反框架
  - 定理: ⊢ φ → ◇φ
- **S4系统**: T + 4公理
  - 对应自反且传递的框架
  - 正内省: ⊢ □φ → □□φ
- **S5系统**: S4 + 5公理
  - 对应等价关系框架
  - 负内省: ⊢ ¬□φ → □¬□φ
  - 适用于认知逻辑和时态逻辑

### 5. 重要定理

- **对应定理**: 公理 ↔ 框架性质的一一对应
  - T公理 ⟺ 自反性
  - 4公理 ⟺ 传递性
  - 5公理 ⟺ 欧几里得性
- **可靠性定理**: ⊢ φ ⟹ ⊨ φ
- **完备性定理**: ⊨ φ ⟹ ⊢ φ
- **有穷模型性**: 可满足 ⟹ 在有穷模型上可满足
- **Lindenbaum引理**: 一致集可扩展为极大一致集

### 6. 时态逻辑扩展

- **线性时态逻辑 (LTL)**:
  - X φ (下一时刻)
  - F φ (最终)
  - G φ (总是)
  - φ U ψ (直到)
  - 路径语义: 状态无穷序列
- **计算树逻辑 (CTL)**:
  - 路径量词: A (所有路径), E (存在路径)
  - 时态算子: AX, EX, AF, EF, AG, EG, AU, EU
  - 分支时态性质表达
- **CTL与LTL关系**: 表达能力对比

### 7. 可判定性与复杂性

- **可判定性**: 模态逻辑K的可判定性
- **PSPACE完全性**: K, T, S4的判定问题
- **LTL可满足性**: PSPACE完全
- **CTL模型检测**: P完全

## 使用示例

```lean
import FormalMethods.Logic.Modal

open ModalLogic ModalFormula

-- 证明 K 公理
theorem K_axiom_valid (φ ψ : ModalFormula) :
    ⊢ₖ (□(φ →ₘ ψ) →ₘ (□φ →ₘ □ψ)) := by
  apply KDerives.K_axiom

-- 使用对应定理验证框架性质
theorem reflexive_implies_T (F : KripkeFrame) :
    Reflexive F.rel → F ⊨f (□(var 0) →ₘ var 0) := by
  apply correspondence_T.mp
```

## 扩展方向

1. **类型论**：Martin-Löf Type Theory
2. **证明自动化**：tactic 开发
3. **模型论**：超积、类型空间
4. **程序验证**：Hoare逻辑、分离逻辑
5. **混合逻辑**：@算子、状态命名
6. **动态逻辑**：程序逻辑、霍尔逻辑

## 参考

- Enderton, H. B. "A Mathematical Introduction to Logic"
- Mendelson, E. "Introduction to Mathematical Logic"
- Troelstra, A. S., & Schwichtenberg, H. "Basic Proof Theory"
- Avigad, J. "Mathematical Logic and Computation" (Lean 形式化)
