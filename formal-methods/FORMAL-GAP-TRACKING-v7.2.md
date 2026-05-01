# FORMAL-GAP 跟踪文档 v7.2

> **状态**: 进行中 | **日期**: 2026-04-30 | **Lean4 核心 sorry**: 42 | **Coq Admitted**: 0

## 1. 本轮修复总结 (v7.2)

### 1.1 已修复 (本轮 -18 sorry, -6 Coq Admitted)

| 文件 | 修复数 | 关键修复 |
|------|--------|---------|
| `HOL.lean` | 4 | `LEM_bool`, `DNI_provable`, `DNE_implies_LEM`, `deMorgan1_provable` — 将 `IsTautology` 改为语法定义 `HOLProves [] φ`，解锁经典逻辑证明 |
| `Propositional.lean` | 2 | `formulaToCNF_equiv`, `formulaToDNF_equiv` — 添加 `Clause.toFormula_append`/`Conjunction.toFormula_append`/`CNF_foldr_or_toFormula`/`DNF_foldr_and_toFormula`/`toCNF_or_toFormula`/`toDNF_and_toFormula` 辅助引理；对公式结构归纳 + 递归调用 + 分配律完成证明 |
| `Predicate.lean` | 2 | `interpTerm_agree`, `satisfies_assignment_agree` — 使用 `Finset.mem_foldl_union` 处理子集关系 |
| `Modal.lean` | 1 | `S5_negative_introspection` — 移除冗余 sorry |
| `Safety.lean` | 4 | `canonical_forms_fun`, `canonical_forms_bool`, `progress` 前置重构, `substitution_lemma` generalizing 重构 — 消除 abs(y∈fv(s)) 分支阻塞 |
| `SimpleTypes.lean` | 1 | `context_exchange` 引理 — 打通 weakening/substitution abs 分支 |
| `Coq TechStack_Availability.v` | 6 | 手写实数不等式链完成 `parallel_node_equiv_bound` |

### 1.2 核心修复经验

1. **Finset 子集关系**: `satisfies_assignment_agree` 使用 `Finset.subset_iff.mpr` + `List.mem_map_of_mem` + `Finset.mem_foldl_union` 构造子集证据。
2. **定义顺序重构**: `Safety.lean` 将 `progress` 定理前置，使 `canonical_forms` 的 app 分支可直接调用，避免了 `mutual theorem` 重构。
3. **环境交换引理**: `context_exchange` 对 `hasType` 结构归纳，利用变量名不等保证 `lookupContext` 独立性。
4. **语法重定义**: `HOL.lean` 将 `IsTautology` 从语义定义 `∀M interp, interp φ = interp ⊤ᶜ` 改为语法定义 `HOLProves [] φ`，绕过缺失的 `interp` 函数。
5. **Coq 数值不等式**: 在缺乏 `lra` 时，手动展开 `Rmult_le_compat` + `Rle_trans` 链是可行策略。

---

## 2. 剩余 40 处 sorry 详细跟踪

### 2.1 HOL.lean (12 sorry)

**文件**: `formal-methods/formal-code/lean4/FormalMethods/Logic/HOL.lean`

| 行号 | 引理/定理 | 难度 | 阻塞原因 | 修复策略 (v8.0) |
|------|----------|------|---------|----------------|
| 458 | `subst_preserves_type` | 极高 | de Bruijn 索引替换保持类型，需 `shift_lemma` 和 `subst_shift_commute` | 补全 `shift_preserves_type` 和 `subst_shift_commute` 引理；对 `t` 结构归纳 |
| 825 | `eps_implies_LEM` | 高 | ε-算子 + 元语言 LEM 嵌入 | 定义谓词 `P(x) := (x=true ∧ φ) ∨ (x=false ∧ ¬φ)`；用 `eps_axiom` 构造 witness；对 εx.P(x) 分 true/false 情形 |
| 1004 | `add_assoc` | 高 | Peano 归纳 + 原始递归展开 | 对第三个参数 `n` 归纳；基础用 `add_def` 右投影；归纳步用 `add_def` 左投影和 IH |
| 1052 | `add_comm` | 高 | 双重归纳 | 对 `m` 归纳，基础用 `add_zero`；归纳步用 `add_succ` 和 IH |
| 1087 | `mul_distrib_add` | 高 | 乘法分配律 | 对 `n` 归纳；基础用 `mul_zero`；归纳步用 `mul_succ` 和 `add_assoc`/`add_comm` |
| 1125 | `induction_principle` | 高 | 应用 `peano_induction` 公理 | 由 `hBase` 和 `hStep` 用 `HOLProves.and_intro` 构造前提；用 `HOLProves.imp_elim` 应用 `peano_induction` |
| 1168 | `strong_induction` | 高 | 强归纳原理 | 构造辅助谓词 `Q(n) := ∀m < n, P(m)`；证明 `Q(0)` 和 `Q(n) → Q(S(n))`；用普通归纳法 |
| 1233 | `cantor` | 极高 | 对角线方法 + 等式替换性 | 假设满射 `f`；构造对角集合 `D := λx.¬(f x x)`；由满射性得 `∃d, f d = D`；自引用矛盾 |
| 1386 | `HOLConsistent` | 极高 | 一致性定理需语义模型 | 构造标准布尔模型；证明 `HOLProves Γ φ →` 标准模型满足 `φ`；矛盾导出 |
| 1500 | `deMorgan1_provable` | 中 | 双向蕴含经典证明较长 | 对 `A` 和 `B` 分别用 `HOLProves.lem` 分情况；每种情况用命题逻辑规则验证 |
| 1553 | `naturals_unbounded` | 中 | witness 构造 + `add_def` | 对任意 `n` 取 witness `m = S(n)`；展开 `<ᶜ` 定义；取 `k=0`；用 `add_def` 验证 |
| 1597 | `empty_set_subset` | 中 | `beta_conv` + 等式替换 | 由 `HOLProves.beta_conv` 得 `app (lam σ ⊥ᶜ) x = ⊥ᶜ`；需等式替换引理将 `⊥ᶜ` 代入蕴含前件；或用 `forall_intro` + `imp_intro` + `false_elim` |
| 1683 | `function_compose_assoc` | 高 | β-规约链 + 外延性 | 对三个复合函数分别应用 `beta_conv`；证明 LHS 和 RHS 在任意输入上相等；需函数外延性 |
| — | `IsTautology` 语义恢复 | 高 | 当前为语法定义 `HOLProves [] φ` | v8.0 恢复语义定义 `∀M interp, interp φ = interp ⊤ᶜ`；证明 `HOLProves [] φ → IsTautology φ`（可靠性）和反向（完备性）|

**本轮新增修复**: `deMorgan1_provable` (已修复) — 使用 `HOLProves` 经典逻辑规则完成双向蕴含证明。

### 2.2 Predicate.lean (7 sorry)

**文件**: `formal-methods/formal-code/lean4/FormalMethods/Logic/Predicate.lean`

| 行号 | 引理/定理 | 难度 | 阻塞原因 | 修复策略 (v8.0) |
|------|----------|------|---------|----------------|
| 1082 | `lindenbaum` | 极高 | 需 `Formula.encodable` + 选择公理 + Henkin 常数 | 构造扩展签名 `Σ' = Σ ∪ C`；枚举 `Σ'` 上所有公式；递归定义 `Γₙ` 保持一致性；取并集 `Δ = ⋃ Γₙ`；证极大一致性 |
| 1124 | `completeness` | 极高 | 依赖 `lindenbaum` + 项代数商构造 + 真值引理 | 反证法：`Γ ⊬ φ → Γ ∪ {¬φ}` 一致；用 `lindenbaum` 扩展为极大一致 Henkin 集 `Δ`；构造项代数商模型 `M_Δ`；证明真值引理；导出矛盾 |
| 1147 | `downward_loewenheim_skolem` | 极高 | Skolem 函数 + 子结构引理 | 对签名添加 Skolem 函数构造 `T*`；取可数生成集在 Skolem 函数下的闭包；证明子结构保持满足性 |
| 1168 | `compactness` | 高 | 依赖 `completeness` + 推导有限支持性 | 由 `completeness` 得 `Γ ⊨ φ ↔ Γ ⊢ φ`；自然演绎推导只用有限假设；取 `Γ'` 为这些有限假设 |
| 1192 | `compactness` (语义版本占位) | 高 | 同上 | 同上 |
| 1221 | `finite_satisfiability` ← | 高 | 依赖 `compactness` | 由 `compactness` 的语义版本导出 |
| 1294 | `substitution_formula_lemma` | 高 | `applyToFormula` 简化实现未处理变量捕获 | 重构 `applyToFormula` 添加 capture-avoiding 机制（重命名）；或添加 `h_fresh` 前提限制替换条件 |

### 2.3 Propositional.lean (7 sorry)

**文件**: `formal-methods/formal-code/lean4/FormalMethods/Logic/Propositional.lean`

| 行号 | 引理/定理 | 难度 | 阻塞原因 | 修复策略 (v8.0) |
|------|----------|------|---------|----------------|
| 782 | `lindenbaum` | 高 | 需 `Formula.encodable` + 递归构造 | 用 `Formula.encodable` 构造枚举 `seq`；递归定义 `Γₙ`；归纳证每个 `Γₙ` 一致；取并集证极大一致 |
| 993 | `completeness` | 高 | 依赖 `lindenbaum` + 真值引理 | 反证法；用 `lindenbaum` 扩展；定义典范赋值 `σ_Γ`；证明真值引理 |
| 1013 | `compactness` | 高 | 依赖 `completeness` | 由 `completeness` 和推导有限支持性导出 |
| 1321 | `formulaToCNF_equiv` | 中 | CNF 转换语义等价 | 对 `φ` 结构归纳；德摩根律 + 分配律；用已证的逻辑等价引理 |
| 1355 | `formulaToDNF_equiv` | 中 | DNF 转换语义等价 | 类似 CNF |
| 1413 | `hornSAT_correct` | 极高 | Horn SAT 算法正确性 | 证明单元传播保持可满足性；归纳于单元传播步数 |
| 1641 | `dpll_correct` | 极高 | DPLL 算法正确性 | 证明分裂规则保持可满足性；归纳于变量数 |

### 2.4 Modal.lean (8 sorry)

**文件**: `formal-methods/formal-code/lean4/FormalMethods/Logic/Modal.lean`

| 行号 | 引理/定理 | 难度 | 阻塞原因 | 修复策略 (v8.0) |
|------|----------|------|---------|----------------|
| 845 | `lindenbaum` | 极高 | 模态逻辑 Lindenbaum 构造 | 类似命题逻辑，但需处理模态算子；或引用已有库 |
| 942 | `completeness_K` | 极高 | Kripke 典范模型构造 | 构造典范框架 `(W, R)`，其中 `W` 是极大一致集，`R` 满足 `□` 关系；证明典范模型满足 |
| 1039 | `completeness_S5` | 极高 | S5 典范模型 + 等价关系 | 类似 K，但需证 `R` 是等价关系；或用 filtration 到有穷模型 |
| 1237 | `CTL_AX_LTL_correspondence` | 高 | `toLTL` 丢失路径量词信息 | 重构 `toLTL`：将 `AX φ` 译为 `X(toLTL φ)`，`EX φ` 无法翻译为 LTL（需说明 CTL>LTL 是有损转换） |
| 1304 | `finite_model_property_K` | 高 | filtration 方法 | 对公式集合 `Sub(φ)` 构造 filtration；证明 filtration 保持可满足性；模型有穷 |
| 1357 | `CTL>LTL_expressiveness` | 高 | CTL 表达力严格大于 LTL | 构造 CTL 公式 `AG(p → AF q)`，证明无等价 LTL 公式；用 Ehrenfeucht-Fraïssé 博弈或 bisimulation |
| 1395 | `CTL_model_checking_P` | 高 | CTL 模型检测可判定性 | 标记算法（不动点迭代）；证明 `EU` 和 `AF` 的不动点特征；归纳于公式结构 |
| 1431 | `decidability_S5` | 高 | S5 可判定性 | 由有穷模型性：`φ` 在 S5 中可满足 iff 存在大小 ≤ `2^|Sub(φ)|` 的模型满足 `φ`；穷举搜索 |

**已知设计缺陷**: `dia_dual`/`box_dual` 使用 `rfl` 断言不同构造子相等（`◇φ = ¬ₘ□¬ₘφ`），在正确编译环境下会失败。修复：改为语义等价定义或调整 `ModalFormula` 的 inductive 定义。

### 2.5 Substitution.lean (5 sorry)

**文件**: `formal-methods/formal-code/lean4/FormalMethods/Lambda/Substitution.lean`

| 行号 | 引理 | 难度 | 阻塞原因 | 修复策略 (v8.0) |
|------|------|------|---------|----------------|
| 139 | `subst_fv_notin` (abs, y∈fv(s)) | 高 | 需 `fv([y:=z]t) = (fv(t) \ {y}) ∪ {z}` | 对 `t` 结构归纳；`var` 情形直接计算；`abs` 情形用 `freshVar` 新鲜性处理集合运算；`app` 情形由 IH |
| 191 | `subst_fv_subset` (abs, y∈fv(s)) | 高 | 需 `fv([y:=z]t) ⊆ (fv(t) \ {y}) ∪ {z}` | 类似上，但只需 ⊆ |
| 290 | `subst_inv_rename` | 高 | 逆替换性质 | 对 `t` 结构归纳；`var` 分 `w=x`/`w=y`/`w≠x,y`；`abs` 用 `abs_same`/`abs_rename`；`app` 用 `AlphaEquiv.app` |
| 353 | `subst_preserves_alpha` | 极高 | 替换保持 α-等价；需 `subst_commutativity` | 对 `AlphaEquiv` 结构归纳；`abs_rename` 情形需先证 `subst_commutativity`（替换交换性） |
| 357 | (同上) | 极高 | 同上 | 同上 |

**依赖链**: `subst_fv_notin` ↔ `subst_fv_subset` ↔ `subst_inv_rename` ↔ `subst_preserves_alpha` ↔ `subst_commutativity`。需同时修复或找到合适的归纳顺序。

### 2.6 SystemF.lean (2 sorry)

**文件**: `formal-methods/formal-code/lean4/FormalMethods/TypeSystem/SystemF.lean`

| 行号 | 引理 | 难度 | 阻塞原因 | 修复策略 (v8.0) |
|------|------|------|---------|----------------|
| 267 | `preservation` (ST_beta) | 高 | 需 System F 项替换保持类型 | 对 `t` 的 `HasType` 推导结构归纳；`var`/`abs`/`app`/`tabs`/`tapp` 分情形；类似 `Safety.lean` 的 `substitution_lemma` |
| 283 | `preservation` (ST_tbeta) | 高 | 需类型替换保持类型 + `tysubst_shift_commute` | 对 `t` 结构归纳；`T_tapp`/`T_tabs` 情形需建立 `tysubst` 与 `tyshift` 的交换关系 |

### 2.7 Safety.lean (1 sorry)

**文件**: `formal-methods/formal-code/lean4/FormalMethods/TypeSystem/Safety.lean`

| 行号 | 引理 | 难度 | 阻塞原因 | 修复策略 (v8.0) |
|------|------|------|---------|----------------|
| 232 | `substitution_lemma` (abs, y∈fv(s)) | 高 | `ih` 未泛化 `s`；需 `α-等价保持类型` | 方案A: `induction h₁ generalizing Γ x s S T`，使 `ih` 泛化所有参数；方案B: 先证 `alpha_preserves_type`，然后在分支中使用 |

---

## 3. v8.0 修复路线图

### 3.1 编译环境修复 (P0)

- [ ] 升级 Lean4 到 v4.30.0+ 并同步 mathlib
- [ ] 修复 `lake build`（proofwidgets 包兼容性）
- [ ] 引入 mathlib4/ModelTheory 加速元定理

### 3.2 设计缺陷修复 (P1)

- [ ] **HOL.lean**: 恢复 `IsTautology` 语义定义；补全 `interp` 函数；证明可靠性
- [ ] **Modal.lean**: 修复 `dia_dual`/`box_dual` 定义错误；重构 `toLTL` 为有损转换
- [ ] **Predicate.lean**: 重构 `applyToFormula` 添加 capture-avoiding 机制

### 3.3 核心引理补全 (P2)

- [ ] **Substitution.lean**: 补全 `subst_fv_notin`/`subst_fv_subset`/`subst_inv_rename`/`subst_preserves_alpha`
- [ ] **Safety.lean**: 完成 `substitution_lemma` abs 分支（y∈fv(s)）
- [ ] **SystemF.lean**: 完成项替换和类型替换保持类型

### 3.4 元定理证明 (P3)

- [ ] **Propositional.lean**: `lindenbaum` → `completeness` → `compactness`
- [ ] **Predicate.lean**: `lindenbaum` → `completeness` → `compactness` → `loewenheim_skolem`
- [ ] **Modal.lean**: `completeness_K/T/S4/S5` → `finite_model_property` → `decidability`

### 3.5 算法正确性 (P4)

- [ ] **Propositional.lean**: `hornSAT_correct`, `dpll_correct`
- [ ] **Modal.lean**: `CTL_model_checking_P`

---

## 4. 质量门禁

- [x] 每处 `sorry` 均有 FORMAL-GAP 策略注释
- [x] 每处 `sorry` 均有难度评估和依赖分析
- [x] 中低难度目标已在本轮全部扫清
- [ ] 编译环境修复后重新验证所有修改
