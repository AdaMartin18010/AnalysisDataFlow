# 文档-代码一致性检查报告

**生成时间**: 2026-04-10T20:03:56.319335

## 📊 检查摘要

| 指标 | 数值 |
|------|------|
| 扫描文档文件数 | 78 |
| 扫描 Lean 文件数 | 12 |
| 文档形式化引用数 | 6704 |
| Lean 定义/定理数 | 250 |

## ✅ 一致性统计

| 类别 | 数量 | 占比 |
|------|------|------|
| 已对应 (文档↔代码) | 0 | 0.0% |
| 仅文档引用 | 2553 | 38.1% |
| 仅代码实现 | 217 | - |

### 按类型统计

| 类型 | 已对应数量 |
|------|------------|
| 定理 (Thm) | 0 |
| 定义 (Def) | 0 |
| 引理 (Lemma) | 0 |
| 命题 (Prop) | 0 |
| 推论 (Cor) | 0 |

## 🟡 文档有引用但代码缺失

以下形式化元素在文档中有引用，但在 Lean 代码中未找到对应实现：

| 形式化编号 | 文档位置 | 上下文 |
|------------|----------|--------|
| `Cor-F-02-01` | formal-methods\theorem-validator-report.md:23 | | `Cor-F-02-01` | 2 | FAQ.md:125, THEOREM-REGISTRY.md:3177 |... |
| `Cor-F-04-01` | formal-methods\theorem-validator-report.md:24 | | `Cor-F-04-01` | 5 | USTM-F-Reconstruction\04-encoding-veri... |
| `Cor-F-04-02` | formal-methods\theorem-validator-report.md:25 | | `Cor-F-04-02` | 5 | USTM-F-Reconstruction\04-encoding-veri... |
| `Cor-F-04-03` | formal-methods\theorem-validator-report.md:26 | | `Cor-F-04-03` | 5 | USTM-F-Reconstruction\04-encoding-veri... |
| `Cor-F-06-01` | formal-methods\theorem-validator-report.md:27 | | `Cor-F-06-01` | 4 | FORMAL-ELEMENT-ADVANCED-REPORT.md:25, ... |
| `Cor-F-06-02` | formal-methods\theorem-validator-report.md:28 | | `Cor-F-06-02` | 4 | FORMAL-ELEMENT-ADVANCED-REPORT.md:26, ... |
| `Cor-F-06-03` | formal-methods\theorem-validator-report.md:29 | | `Cor-F-06-03` | 4 | FORMAL-ELEMENT-ADVANCED-REPORT.md:27, ... |
| `Cor-F-06-04` | formal-methods\theorem-validator-report.md:30 | | `Cor-F-06-04` | 3 | FORMAL-ELEMENT-ADVANCED-REPORT.md:28, ... |
| `Cor-F-06-05` | formal-methods\theorem-validator-report.md:31 | | `Cor-F-06-05` | 3 | FORMAL-ELEMENT-ADVANCED-REPORT.md:29, ... |
| `Cor-F-06-06` | formal-methods\theorem-validator-report.md:32 | | `Cor-F-06-06` | 3 | FORMAL-ELEMENT-ADVANCED-REPORT.md:30, ... |
| `Cor-F-06-50` | formal-methods\theorem-validator-report.md:33 | | `Cor-F-06-50` | 4 | FORMAL-ELEMENT-ADVANCED-REPORT.md:31, ... |
| `Cor-F-09-05` | formal-methods\theorem-validator-report.md:34 | | `Cor-F-09-05` | 50 | FORMAL-ELEMENT-ADVANCED-REPORT.md:32,... |
| `Cor-F-12-05` | formal-methods\theorem-validator-report.md:35 | | `Cor-F-12-05` | 13 | FORMAL-ELEMENT-ADVANCED-REPORT.md:33,... |
| `Cor-K-10-13` | formal-methods\theorem-validator-report.md:36 | | `Cor-K-10-13` | 3 | FORMAL-ELEMENT-ADVANCED-REPORT.md:34, ... |
| `Cor-S-01-01` | formal-methods\theorem-validator-report.md:37 | | `Cor-S-01-01` | 2 | MAINTENANCE-GUIDE.md:180, THEOREM-REGI... |
| `Cor-S-02-01` | formal-methods\theorem-validator-report.md:38 | | `Cor-S-02-01` | 32 | AGENTS.md:40, CONTRIBUTING-EN.md:224 ... |
| `Cor-S-02-04` | formal-methods\theorem-validator-report.md:39 | | `Cor-S-02-04` | 5 | FORMAL-ELEMENT-ADVANCED-REPORT.md:130,... |
| `Cor-S-02-05` | formal-methods\theorem-validator-report.md:40 | | `Cor-S-02-05` | 5 | FORMAL-ELEMENT-ADVANCED-REPORT.md:131,... |
| `Cor-S-02-06` | formal-methods\theorem-validator-report.md:41 | | `Cor-S-02-06` | 5 | FORMAL-ELEMENT-ADVANCED-REPORT.md:132,... |
| `Cor-S-03-03` | formal-methods\theorem-validator-report.md:42 | | `Cor-S-03-03` | 2 | i18n\en\Struct\Key-Theorem-Proof-Chain... |
| `Cor-S-04-01` | formal-methods\theorem-validator-report.md:43 | | `Cor-S-04-01` | 3 | KNOWLEDGE-GRAPH-GUIDE.md:154, RELATION... |
| `Cor-S-04-02` | formal-methods\theorem-validator-report.md:44 | | `Cor-S-04-02` | 2 | DESIGN-PRINCIPLES.md:340, THEOREM-REGI... |
| `Cor-S-04-08` | formal-methods\04-application-layer\08-async-semantics\01-async-formalization.md:411 | **推论 Cor-S-04-08-01 (多线程非确定性来源)**... |
| `Cor-S-05-05` | formal-methods\05-verification\04-security\01-information-flow-security.md:508 | > **Cor-S-05-05-01** [无 stuck 状态]: 良类型的程序不会进入非终止的非法状态（不考虑无限循... |
| `Cor-S-07-01` | formal-methods\mermaid-validator-report.md:538762 | - Chinese text in node should be quoted: 'Cor-S-07-01<br/>容错... |
| `Cor-S-07-02` | formal-methods\theorem-validator-report.md:46 | | `Cor-S-07-02` | 16 | FORMAL-ELEMENT-ADVANCED-REPORT.md:37,... |
| `Cor-S-07-03` | formal-methods\theorem-validator-report.md:47 | | `Cor-S-07-03` | 6 | FORMAL-ELEMENT-ADVANCED-REPORT.md:38, ... |
| `Cor-S-14-01` | formal-methods\theorem-validator-report.md:48 | | `Cor-S-14-01` | 21 | cross-ref-validation-report-v2.md:264... |
| `Cor-S-15-01` | formal-methods\theorem-validator-report.md:49 | | `Cor-S-15-01` | 15 | cross-ref-validation-report-v2.md:266... |
| `Cor-S-18-01` | formal-methods\theorem-validator-report.md:50 | | `Cor-S-18-01` | 4 | FORMAL-ELEMENT-ADVANCED-REPORT.md:41, ... |
| `Cor-S-22-01` | formal-methods\theorem-validator-report.md:51 | | `Cor-S-22-01` | 13 | FORMAL-ELEMENT-ADVANCED-REPORT.md:42,... |
| `Cor-S-23-01` | formal-methods\theorem-validator-report.md:52 | | `Cor-S-23-01` | 15 | FORMAL-ELEMENT-ADVANCED-REPORT.md:43,... |
| `Cor-S-25-01` | formal-methods\theorem-validator-report.md:53 | | `Cor-S-25-01` | 15 | cross-ref-validation-report-v2.md:282... |
| `Cor-S-25-02` | formal-methods\theorem-validator-report.md:54 | | `Cor-S-25-02` | 15 | cross-ref-validation-report-v2.md:282... |
| `Cor-S-29-01` | formal-methods\theorem-validator-report.md:55 | | `Cor-S-29-01` | 5 | FORMAL-ELEMENT-ADVANCED-REPORT.md:46, ... |
| `Cor-S-98-01` | formal-methods\theorem-validator-report.md:56 | | `Cor-S-98-01` | 2 | formal-methods\98-appendices\wikipedia... |
| `Def-F-00-01` | formal-methods\theorem-validator-report.md:57 | | `Def-F-00-01` | 7 | FORMAL-ELEMENT-ADVANCED-REPORT.md:47, ... |
| `Def-F-00-02` | formal-methods\theorem-validator-report.md:58 | | `Def-F-00-02` | 6 | FORMAL-ELEMENT-ADVANCED-REPORT.md:48, ... |
| `Def-F-00-03` | formal-methods\theorem-validator-report.md:59 | | `Def-F-00-03` | 6 | FORMAL-ELEMENT-ADVANCED-REPORT.md:49, ... |
| `Def-F-00-04` | formal-methods\theorem-validator-report.md:60 | | `Def-F-00-04` | 6 | FORMAL-ELEMENT-ADVANCED-REPORT.md:50, ... |
| `Def-F-00-05` | formal-methods\theorem-validator-report.md:61 | | `Def-F-00-05` | 6 | FORMAL-ELEMENT-ADVANCED-REPORT.md:51, ... |
| `Def-F-01-01` | formal-methods\theorem-validator-report.md:62 | | `Def-F-01-01` | 27 | FORMAL-ELEMENT-ADVANCED-REPORT.md:52,... |
| `Def-F-01-02` | formal-methods\INDEX.md:68 | | Def-F-01-02 | 完全偏序(CPO) | 01-foundations/01-order-theory.m... |
| `Def-F-01-03` | formal-methods\theorem-validator-report.md:64 | | `Def-F-01-03` | 24 | FORMAL-ELEMENT-ADVANCED-REPORT.md:54,... |
| `Def-F-01-04` | formal-methods\theorem-validator-report.md:65 | | `Def-F-01-04` | 24 | FORMAL-ELEMENT-ADVANCED-REPORT.md:55,... |
| `Def-F-01-05` | formal-methods\theorem-validator-report.md:66 | | `Def-F-01-05` | 19 | FORMAL-ELEMENT-ADVANCED-REPORT.md:56,... |
| `Def-F-01-06` | formal-methods\theorem-validator-report.md:67 | | `Def-F-01-06` | 22 | FORMAL-ELEMENT-ADVANCED-REPORT.md:57,... |
| `Def-F-01-07` | formal-methods\theorem-validator-report.md:68 | | `Def-F-01-07` | 3 | formal-methods\01-foundations\01-order... |
| `Def-F-01-08` | formal-methods\theorem-validator-report.md:69 | | `Def-F-01-08` | 3 | formal-methods\01-foundations\01-order... |
| `Def-F-01-09` | formal-methods\theorem-validator-report.md:70 | | `Def-F-01-09` | 3 | formal-methods\01-foundations\01-order... |
| ... | ... | 还有 2503 项 |

## 🔵 代码有实现但文档未引用

以下 Lean 实现在代码中存在，但文档中未引用对应的形式化编号：

| 名称 | 类型 | 文件位置 |
|------|------|----------|
| `Transition` | def | formal-methods\formal-code\lean4\FormalMethods\Concurrent.lean:36 |
| `StrongBisimulation` | def | formal-methods\formal-code\lean4\FormalMethods\Concurrent.lean:60 |
| `StrongBisimilar` | def | formal-methods\formal-code\lean4\FormalMethods\Concurrent.lean:68 |
| `WeakBisimulation` | def | formal-methods\formal-code\lean4\FormalMethods\Concurrent.lean:78 |
| `WeakBisimilar` | def | formal-methods\formal-code\lean4\FormalMethods\Concurrent.lean:90 |
| ... | ... | 还有 4 项 |
| `Channel` | def | formal-methods\formal-code\lean4\FormalMethods\Concurrent\CCS.lean:17 |
| `ConstName` | def | formal-methods\formal-code\lean4\FormalMethods\Concurrent\CCS.lean:21 |
| `complement` | def | formal-methods\formal-code\lean4\FormalMethods\Concurrent\CCS.lean:47 |
| `complement_involutive` | lemma | formal-methods\formal-code\lean4\FormalMethods\Concurrent\CCS.lean:53 |
| `areComplementary` | def | formal-methods\formal-code\lean4\FormalMethods\Concurrent\CCS.lean:62 |
| ... | ... | 还有 22 项 |
| `I` | def | formal-methods\formal-code\lean4\FormalMethods\Lambda.lean:25 |
| `tru` | def | formal-methods\formal-code\lean4\FormalMethods\Lambda.lean:29 |
| `fls` | def | formal-methods\formal-code\lean4\FormalMethods\Lambda.lean:33 |
| `cond` | def | formal-methods\formal-code\lean4\FormalMethods\Lambda.lean:37 |
| `beta_star_refl` | lemma | formal-methods\formal-code\lean4\FormalMethods\Lambda\Reduction.lean:92 |
| `beta_star_trans` | lemma | formal-methods\formal-code\lean4\FormalMethods\Lambda\Reduction.lean:98 |
| `beta_step_to_star` | lemma | formal-methods\formal-code\lean4\FormalMethods\Lambda\Reduction.lean:111 |
| `isNormalForm` | def | formal-methods\formal-code\lean4\FormalMethods\Lambda\Reduction.lean:127 |
| `isValue` | def | formal-methods\formal-code\lean4\FormalMethods\Lambda\Reduction.lean:135 |
| ... | ... | 还有 5 项 |
| `subst` | def | formal-methods\formal-code\lean4\FormalMethods\Lambda\Substitution.lean:41 |
| `subst_var_neq` | lemma | formal-methods\formal-code\lean4\FormalMethods\Lambda\Substitution.lean:73 |
| `subst_var_eq` | lemma | formal-methods\formal-code\lean4\FormalMethods\Lambda\Substitution.lean:82 |
| `subst_fv_notin` | lemma | formal-methods\formal-code\lean4\FormalMethods\Lambda\Substitution.lean:91 |
| `subst_fv_subset` | lemma | formal-methods\formal-code\lean4\FormalMethods\Lambda\Substitution.lean:122 |
| ... | ... | 还有 3 项 |
| `mkVar` | def | formal-methods\formal-code\lean4\FormalMethods\Lambda\Syntax.lean:45 |
| `mkAbs` | def | formal-methods\formal-code\lean4\FormalMethods\Lambda\Syntax.lean:48 |
| `mkApp` | def | formal-methods\formal-code\lean4\FormalMethods\Lambda\Syntax.lean:51 |
| `identity` | def | formal-methods\formal-code\lean4\FormalMethods\Lambda\Syntax.lean:60 |
| `omegaTerm` | def | formal-methods\formal-code\lean4\FormalMethods\Lambda\Syntax.lean:64 |
| ... | ... | 还有 15 项 |
| `Assignment` | def | formal-methods\formal-code\lean4\FormalMethods\Logic.lean:65 |
| `eval` | def | formal-methods\formal-code\lean4\FormalMethods\Logic.lean:70 |
| `valid` | def | formal-methods\formal-code\lean4\FormalMethods\Logic.lean:85 |
| `satisfiable` | def | formal-methods\formal-code\lean4\FormalMethods\Logic.lean:93 |
| `entails` | def | formal-methods\formal-code\lean4\FormalMethods\Logic.lean:101 |
| ... | ... | 还有 3 项 |
| `PropVar` | def | formal-methods\formal-code\lean4\FormalMethods\Logic\Propositional.lean:27 |
| `toString` | def | formal-methods\formal-code\lean4\FormalMethods\Logic\Propositional.lean:32 |
| `iff` | def | formal-methods\formal-code\lean4\FormalMethods\Logic\Propositional.lean:59 |
| `vars` | def | formal-methods\formal-code\lean4\FormalMethods\Logic\Propositional.lean:67 |
| `depth` | def | formal-methods\formal-code\lean4\FormalMethods\Logic\Propositional.lean:77 |
| ... | ... | 还有 88 项 |
| `substitution_lemma` | lemma | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\Safety.lean:47 |
| `preservation` | theorem | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\Safety.lean:72 |
| `preservation_star` | theorem | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\Safety.lean:111 |
| `canonical_forms_fun` | lemma | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\Safety.lean:136 |
| `canonical_forms_bool` | lemma | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\Safety.lean:148 |
| ... | ... | 还有 2 项 |
| `Context` | def | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\SimpleTypes.lean:59 |
| `emptyContext` | def | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\SimpleTypes.lean:64 |
| `extendContext` | def | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\SimpleTypes.lean:71 |
| `lookupContext` | def | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\SimpleTypes.lean:79 |
| `inContext` | def | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\SimpleTypes.lean:93 |
| ... | ... | 还有 7 项 |
| `tyshift` | def | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\SystemF.lean:32 |
| `tysubst` | def | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\SystemF.lean:39 |
| `tysubst_top` | def | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\SystemF.lean:46 |
| `tmshift` | def | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\SystemF.lean:49 |
| `tmsubst` | def | formal-methods\formal-code\lean4\FormalMethods\TypeSystem\SystemF.lean:63 |
| ... | ... | 还有 13 项 |
| `main` | def | formal-methods\formal-code\lean4\Main.lean:37 |

## 💡 改进建议

1. **补充代码实现**: 为 2553 个文档引用的形式化元素创建 Lean 实现

2. **补充文档引用**: 为 217 个代码实现添加文档中的形式化编号引用

---
*报告由 doc-code-consistency.py 自动生成*
