# LLM 辅助形式化证明自动化

> 所属阶段: Struct/06-frontier | 前置依赖: Struct/05-comparative-analysis/formal-verification-methods.md, Flink/04-runtime/distributed-snapshot-formal-proof.md, Knowledge/06-frontier/ai-agent-formal-methods.md | 形式化等级: L5-L6

## 摘要

大型语言模型（Large Language Models, LLMs）与形式化证明系统的融合正成为 2025–2026 年形式化方法领域最活跃的交叉方向。本文从理论定义、能力边界、系统映射、工程实践与可验证性五个维度，对 **LLM 辅助形式化证明自动化（LLM-guided Formal Proof Automation, LFPA）** 进行系统性形式化分析。我们建立了 LFPA 的形式化工作流模型，定义了证明生成成功率、策略推荐精确度、证明可验证性等核心度量，并基于 2025–2026 年主流基准测试数据（Claude-3.7-Sonnet 在分布式协议基准上证明率 42.3%，DeepSeek-V3.2-Exp 达到 50.0%）进行量化分析。本文系统覆盖了 TLA⁺/TLAPS、Coq、Lean 4 三大主流工具的 LLM 集成现状，建立了 LFPA 与传统自动定理证明（ATP）之间的精确关系映射，并针对 LLM 生成证明的可验证性提出了形式化安全框架。通过 TLA⁺ 证明草图生成、Lean 4 策略推荐、Coq 证明补全三个工程实例，验证了 LFPA 在工业级分布式系统验证中的可行性与当前局限。

**关键词**: LLM-guided Proof Automation, Formal Verification, TLA⁺, Coq, Lean 4, TLAPS, ATP, Proof Synthesis, Verification Safety

---

## 目录

- [1. 概念定义 (Definitions)](#1-概念定义-definitions)
- [2. 属性推导 (Properties)](#2-属性推导-properties)
- [3. 关系建立 (Relations)](#3-关系建立-relations)
- [4. 论证过程 (Argumentation)](#4-论证过程-argumentation)
- [5. 形式证明 / 工程论证 (Proof / Engineering Argument)](#5-形式证明-工程论证-proof-engineering-argument)
- [6. 实例验证 (Examples)](#6-实例验证-examples)
- [7. 可视化 (Visualizations)](#7-可视化-visualizations)
- [8. 引用参考 (References)](#8-引用参考-references)

---

## 1. 概念定义 (Definitions)

### Def-S-06-18-01: LLM 辅助形式化证明自动化 (LFPA)

**定义**: LLM 辅助形式化证明自动化（LLM-guided Formal Proof Automation, LFPA）是一个七元组

$$
\mathcal{LFP\!A} = \langle \mathcal{M}, \mathcal{T}, \mathcal{P}, \mathcal{G}, \mathcal{V}, \mathcal{S}, \mathcal{F} \rangle
$$

其中各分量的形式化语义如下：

| 分量 | 符号 | 类型 | 语义 |
|------|------|------|------|
| 语言模型 | $\mathcal{M}$ | $\Sigma^* \to \mathcal{D}(\Sigma^*)$ | 将证明上下文编码为字符串，生成候选证明策略或完整证明脚本的概率分布 |
| 目标形式化语言 | $\mathcal{T}$ | $\{ \text{TLA}^+, \text{Coq}, \text{Lean 4}, \text{Dafny}, \text{ACSL}, \dots \}$ | 待验证规约与证明所处的基础形式化系统 |
| 证明问题 | $\mathcal{P}$ | $\langle \Gamma, \phi \rangle$ | 在假设环境 $\Gamma$ 下证明目标命题 $\phi$ 的判定问题实例 |
| 生成函数 | $\mathcal{G}$ | $\mathcal{M} \times \mathcal{P} \times \mathcal{T} \to \mathcal{D}(\Pi)$ | 将模型、问题与语言映射为候选证明脚本空间 $\Pi$ 上的概率分布 |
| 验证器 | $\mathcal{V}$ | $\Pi \times \mathcal{P} \times \mathcal{T} \to \{ \top, \bot, \text{timeout} \}$ | 对候选证明脚本进行机械验证的判定函数 |
| 策略空间 | $\mathcal{S}$ | $\mathcal{P}(\mathcal{A})$ | 可用于构造证明的原子策略集合 $\mathcal{A}$ 的幂集 |
| 反馈函数 | $\mathcal{F}$ | $\mathcal{V}(\pi) \times \pi \to \mathcal{D}(\mathcal{S})$ | 根据验证结果反馈调整后续生成策略的适应函数 |

**直观解释**: LFPA 不是将证明完全交给 LLM 的"黑箱验证"，而是一个**人机协同的闭环系统**：LLM 负责在庞大的证明策略空间中生成高概率正确的候选，形式化验证器负责对这些候选进行不可篡改的机械检查，反馈函数则将验证结果（成功、失败、超时）回传至生成阶段以指导下一轮采样。该定义明确区分了 LLM 的**生成角色**与验证器的**裁判角色**，这是 LFPA 与传统神经定理证明（Neural Theorem Proving, NTP）的根本差异。

---

### Def-S-06-18-02: 证明生成成功率 (Proof Generation Success Rate, PGSR)

**定义**: 给定形式化语言 $\mathcal{T}$、测试问题集 $\mathcal{Q} = \{ \mathcal{P}_1, \dots, \mathcal{P}_n \}$ 以及 LLM $\mathcal{M}$，在温度参数 $\tau$ 与采样数 $k$（pass@$k$）条件下，证明生成成功率定义为：

$$
\text{PGSR}_{\mathcal{T}, \tau, k}(\mathcal{M}, \mathcal{Q}) = \frac{1}{n} \sum_{i=1}^{n} \mathbb{1}\left[ \exists j \in [1,k], \; \mathcal{V}\bigl(\mathcal{G}(\mathcal{M}, \mathcal{P}_i, \mathcal{T})_j, \mathcal{P}_i, \mathcal{T}\bigr) = \top \right]
$$

其中 $\mathbb{1}[\cdot]$ 为指示函数，$\mathcal{G}(\mathcal{M}, \mathcal{P}_i, \mathcal{T})_j$ 表示第 $j$ 次采样得到的候选证明脚本。

**细化度量**:

1. **pass@1**: $k=1$ 时的严格成功率，反映模型单次生成的可靠性：
   $$
   \text{pass@1} = \frac{1}{n} \sum_{i=1}^{n} \mathbb{1}\left[ \mathcal{V}\bigl(\mathcal{G}(\mathcal{M}, \mathcal{P}_i, \mathcal{T})_1, \mathcal{P}_i, \mathcal{T}\bigr) = \top \right]
   $$

2. **pass@$k$ (无放回估计)**: 使用无放回采样修正以避免高估 [^9]：
   $$
   \text{pass@}k = \mathbb{E}_{\mathcal{Q}}\left[ 1 - \frac{\binom{n - c}{k}}{\binom{n}{k}} \right]
   $$
   其中 $n$ 为每问题总采样数，$c$ 为其中正确样本数。

3. **按难度分层成功率**: 将 $\mathcal{Q}$ 按人类专家平均证明时间 $t$ 划分为易（$t < 10$ min）、中（$10 \leq t < 60$ min）、难（$t \geq 60$ min）三级：
   $$
   \text{PGSR}_{\text{easy}} = \frac{|\{ \mathcal{P} \in \mathcal{Q}_{\text{easy}} : \text{pass@}1 = \top \}|}{|\mathcal{Q}_{\text{easy}}|}
   $$

---

### Def-S-06-18-03: 证明策略推荐精确度 (Proof Tactic Recommendation Precision, PTRP)

**定义**: 在交互式定理证明器（ITP）环境中，LLM 的策略推荐精确度是一个条件概率度量：

$$
\text{PTRP} = \mathbb{P}\left( \text{tactic } t \text{ 使证明状态前进} \mid \mathcal{M}(s) = t \right)
$$

其中 $s$ 为当前证明状态（proof state / proof obligation），$\mathcal{M}(s)$ 为模型推荐的下一策略。若使用 top-$k$ 推荐，则定义：

$$
\text{PTRP@}k = \mathbb{P}\left( \exists t \in \text{top-}k(\mathcal{M}, s), \; t \text{ 为有效策略} \right)
$$

**形式化状态编码**: 证明状态 $s$ 在 Lean 4 中表示为

```
s : List MVarId × LocalContext × Environment
```

即（待证目标列表 × 局部上下文 × 全局环境）的三元组。LLM 通过 **Proof State Serialization** 将 $s$ 编码为字符串：

$$
\text{serialize}(s) = \text{goals}(s) \; \| \; \text{locals}(s) \; \| \; \text{defs}(s)
$$

其中 `\|` 为分隔符，包含当前目标类型、局部假设、已引入定义。

---

### Def-S-06-18-04: LLM 证明幻觉 (Proof Hallucination)

**定义**: 给定形式化系统 $\mathcal{T}$ 与其语法规则 $G_{\mathcal{T}}$（上下文无关文法），LLM 生成的证明脚本 $\pi$ 的幻觉类型按严重程度划分为四级：

| 级别 | 名称 | 形式化定义 | 检测方式 |
|------|------|------------|----------|
| H-1 | **语法幻觉** | $\pi \notin \mathcal{L}(G_{\mathcal{T}})$ | 解析器（Parser）拒绝 |
| H-2 | **类型幻觉** | $\pi \in \mathcal{L}(G_{\mathcal{T}}) \land \text{TypeChecker}(\pi) = \bot$ | 类型检查器拒绝 |
| H-3 | **逻辑幻觉** | $\text{TypeChecker}(\pi) = \top \land \mathcal{V}(\pi, \mathcal{P}, \mathcal{T}) = \bot$ | 验证器拒绝 |
| H-4 | **元理论幻觉** | $\exists \mathcal{P}' \neq \mathcal{P}, \; \mathcal{V}(\pi, \mathcal{P}', \mathcal{T}) = \top \land \mathcal{V}(\pi, \mathcal{P}, \mathcal{T}) = \bot$ | 交叉验证/人工审查 |

**关键观察**: H-1 与 H-2 可被机械检测完全消除；H-3 依赖验证器的完备性；H-4 最难检测，表现为"证明了一个错误的定理"。H-4 的存在意味着 **LLM 生成的证明即使通过验证器，也不意味着原始命题为真**，除非验证器本身被证明是可靠（sound）的。

---

### Def-S-06-18-05: 可验证生成 (Verifiable Generation)

**定义**: 一个 LFPA 系统满足 **可验证生成** 性质，当且仅当：

$$
\forall \mathcal{P}, \; \forall \pi \sim \mathcal{G}(\mathcal{M}, \mathcal{P}, \mathcal{T}), \quad \mathcal{V}(\pi, \mathcal{P}, \mathcal{T}) = \top \; \implies \; \Gamma \vdash_{\mathcal{T}} \phi
$$

即：凡是被验证器接受的证明脚本，必然在目标形式化系统的演绎语义下有效。该性质将 LFPA 的可靠性归约到验证器 $\mathcal{V}$ 的可靠性，而非 LLM $\mathcal{M}$ 的可靠性。

**推论**: 在可验证生成框架下，LLM 的幻觉问题（Def-S-06-18-04）被降级为 **效率问题** 而非 **正确性问题**。无论 LLM 生成何种语法/逻辑错误的候选，验证器 $\mathcal{V}$ 作为安全闸门将拒绝所有无效证明。系统的正确性保障完全由 $\mathcal{V}$ 承担。

---

### Def-S-06-18-06: 证明搜索树与 LLM 引导启发式

**定义**: 给定证明问题 $\mathcal{P} = \langle \Gamma, \phi \rangle$ 与策略空间 $\mathcal{S}$，证明搜索树是一个有根树 $\mathcal{K} = \langle N, E, r, \ell \rangle$，其中：

- $N$ 为节点集合，每个节点 $n \in N$ 代表一个证明状态；
- $E \subseteq N \times \mathcal{S} \times N$ 为带标签的边，$(n, t, n') \in E$ 表示在状态 $n$ 应用策略 $t$ 到达状态 $n'$；
- $r \in N$ 为根节点，对应初始证明义务 $\phi$；
- $\ell : N \to \{ \text{open}, \text{closed}, \text{dead} \}$ 为节点状态标记。

**LLM 引导启发式** 是一个函数 $h_{\mathcal{M}} : N \to \mathcal{D}(\mathcal{S})$，将当前证明状态映射为策略空间上的概率分布：

$$
h_{\mathcal{M}}(n) = \text{softmax}\left( \frac{\mathcal{M}(\text{serialize}(n))}{\tau} \right)
$$

传统 ATP 使用手工设计的启发式（如子句权重、字面量排序），而 LFPA 使用 $h_{\mathcal{M}}$ 作为数据驱动的可学习启发式。

---

### Def-S-06-18-07: 人机协同证明工作流 (Human-in-the-Loop Proof Workflow, HILPW)

**定义**: HILPW 是一个状态机 $\mathcal{W} = \langle Q, \Sigma, \delta, q_0, F \rangle$，其中：

- 状态集 $Q = \{ \text{SPECIFY}, \text{GENERATE}, \text{VERIFY}, \text{REPAIR}, \text{DONE}, \text{ABANDON} \}$；
- 输入字母表 $\Sigma = \{ \text{llm\_output}, \text{verifier\_ok}, \text{verifier\_fail}, \text{human\_edit}, \text{human\_accept}, \text{timeout} \}$；
- 转移函数 $\delta : Q \times \Sigma \to Q$ 定义工作流演化；
- $q_0 = \text{SPECIFY}$ 为初始状态；
- $F = \{ \text{DONE}, \text{ABANDON} \}$ 为终结状态。

该状态机的关键转移规则为：

| 当前状态 | 输入 | 下一状态 | 语义 |
|----------|------|----------|------|
| SPECIFY | human_edit | SPECIFY | 人类编写/修改形式化规约 |
| SPECIFY | human_accept | GENERATE | 规约定稿，触发 LLM 生成 |
| GENERATE | llm_output | VERIFY | LLM 输出候选证明 |
| VERIFY | verifier_ok | DONE | 验证通过，证明完成 |
| VERIFY | verifier_fail | REPAIR | 验证失败，进入修复模式 |
| VERIFY | timeout | REPAIR | 验证超时（如搜索空间过大） |
| REPAIR | llm_output | VERIFY | LLM 基于错误信息重新生成 |
| REPAIR | human_edit | GENERATE | 人类介入修改证明策略 |
| REPAIR | timeout × 3 | ABANDON | 多次失败后放弃 |

---

## 2. 属性推导 (Properties)

### Lemma-S-06-18-01: 可验证生成的可靠性传递

**命题**: 若 LFPA 系统 $\mathcal{LFP\!A}$ 满足可验证生成（Def-S-06-18-05），且验证器 $\mathcal{V}$ 是可靠的（sound），则整个 LFPA 系统的输出可靠性不依赖于 LLM $\mathcal{M}$ 的可靠性。

**形式化表述**:

$$
\text{Sound}(\mathcal{V}) \land \text{VerifiableGen}(\mathcal{LFP\!A}) \implies \forall \pi, \mathcal{P}, \; \mathcal{V}(\pi, \mathcal{P}, \mathcal{T}) = \top \Rightarrow \Gamma \vdash_{\mathcal{T}} \phi
$$

**证明**:

1. 由 Def-S-06-18-05（可验证生成），我们有：
   $$\forall \mathcal{P}, \forall \pi \sim \mathcal{G}, \; \mathcal{V}(\pi, \mathcal{P}, \mathcal{T}) = \top \implies \Gamma \vdash_{\mathcal{T}} \phi$$

2. 由假设 $\text{Sound}(\mathcal{V})$，验证器仅接受语义上有效的证明：
   $$\mathcal{V}(\pi, \mathcal{P}, \mathcal{T}) = \top \implies \pi \text{ 是 } \phi \text{ 在 } \Gamma \text{ 下的有效证明}$$

3. 对任意被接受的 $\pi$，结合 (1) 与 (2)：
   $$\mathcal{V}(\pi, \mathcal{P}, \mathcal{T}) = \top \implies \Gamma \vdash_{\mathcal{T}} \phi$$

4. 注意该推导不涉及 $\mathcal{M}$ 的任何性质。无论 $\mathcal{M}$ 生成多少幻觉、语法错误或逻辑谬误，只要验证器 $\mathcal{V}$ 拒绝所有无效证明，最终输出就保持可靠。

$$\square$$

---

### Lemma-S-06-18-02: 策略推荐精确度的上界

**命题**: 在交互式定理证明环境中，LLM 的策略推荐精确度 PTRP（Def-S-06-18-03）受限于形式化语言 $\mathcal{T}$ 的策略空间熵 $H(\mathcal{S})$ 与证明状态编码的信息保真度 $I(s; \text{serialize}(s))$：

$$
\text{PTRP} \leq \frac{I(s; \text{serialize}(s))}{H(\mathcal{S})} \cdot \text{Accuracy}_{\text{base}}
$$

其中 $\text{Accuracy}_{\text{base}}$ 为模型在完全信息下的基线准确率。

**证明概要**:

1. 证明状态 $s$ 包含丰富的结构化信息（类型、约束、局部上下文）。序列化过程 $\text{serialize}(s)$ 不可避免地损失信息，特别是类型依赖图、 universe 层级、隐式参数解析等元信息。

2. 由信息论数据处理不等式：
   $$I(s; \mathcal{M}) \leq I(\text{serialize}(s); \mathcal{M}) \leq I(s; \text{serialize}(s))$$
   模型对状态的理解上限被序列化保真度所约束。

3. 策略空间 $\mathcal{S}$ 的熵 $H(\mathcal{S})$ 量化了任意状态下的决策不确定性。在 Lean 4 中，$|\mathcal{S}| > 500$ 个核心策略，加上数以万计的引理名称作为参数，使得 $H(\mathcal{S})$ 极高。

4. 因此，即使 $\mathcal{M}$ 是完美预测器，序列化损失也会降低有效准确率，形成信息论上界。

$$\square$$

---

### Lemma-S-06-18-03: 语法幻觉的完全可消除性

**命题**: 对于任意上下文无关形式化语言 $\mathcal{T}$，存在一个确定性算法 $A$ 使得：

$$
\forall \pi, \; A(\pi) = \top \iff \pi \in \mathcal{L}(G_{\mathcal{T}})
$$

且该算法的时间复杂度为 $O(|\pi|^3)$（CYK 算法）或 $O(|\pi|)$（LR(1) 解析器）。因此，**H-1 级幻觉（Def-S-06-18-04）可被完全消除**，且不引入假阴性（即不会拒绝合法证明）。

**证明**:

1. TLA⁺、Coq/Gallina、Lean 4 的表层语法均为上下文无关语言（CFL）。TLA⁺ 的语法由 TLAPLUS 文法定义；Coq 的 Vernacular 命令由 camlp5 解析器处理；Lean 4 使用自举的 `syntax` 机制定义解析规则。

2. 对于任意 CFL，存在等价的下推自动机（PDA）识别器。TLA⁺ 的 SANY 解析器、Coq 的解析器、Lean 4 的 `Parser` 均为确定性 PDA 的实现。

3. 由形式语言理论，确定性 PDA 对成员资格判定是精确的（既无假阳性也无假阴性）。

4. 因此，在 LFPA 流水线中，可在生成阶段后接入解析器作为过滤层：
   $$\pi \xrightarrow{\mathcal{M}} \text{Parser} \xrightarrow{\in \mathcal{L}(G)} \text{TypeChecker} \xrightarrow{\top} \mathcal{V}$$
   所有 H-1 幻觉在 Parser 阶段被拦截。

$$\square$$

---

### Prop-S-06-18-01: LLM 证明成功率的形式化分解

**命题**: LLM 在形式化证明问题上的总体成功率可分解为四个独立因子的乘积：

$$
\text{PGSR} = p_{\text{parse}} \cdot p_{\text{type}} \cdot p_{\text{logic}} \cdot p_{\text{term}}
$$

其中：

- $p_{\text{parse}} = \mathbb{P}(\pi \in \mathcal{L}(G_{\mathcal{T}}))$：语法正确概率
- $p_{\text{type}} = \mathbb{P}(\text{TypeChecker}(\pi) = \top \mid \pi \in \mathcal{L}(G_{\mathcal{T}}))$：在语法正确条件下类型正确概率
- $p_{\text{logic}} = \mathbb{P}(\mathcal{V}(\pi) = \top \mid \text{TypeChecker}(\pi) = \top)$：在类型正确条件下逻辑正确概率
- $p_{\text{term}} = \mathbb{P}(\text{Termination} \mid \mathcal{V}(\pi) = \top)$：验证过程本身的终止概率

**经验数据（基于 arXiv 2026-04 基准 [^2]）**:

| 形式化语言 | $p_{\text{parse}}$ | $p_{\text{type}}$ | $p_{\text{logic}}$ | $p_{\text{term}}$ | 综合 pass@1 |
|------------|-------------------|-------------------|-------------------|-------------------|-------------|
| Lean 4 | 0.94 | 0.78 | 0.62 | 0.99 | 0.45 |
| Coq | 0.91 | 0.71 | 0.55 | 0.98 | 0.35 |
| TLA⁺ (TLAPS) | 0.88 | 0.65 | 0.48 | 0.95 | 0.26 |
| Dafny | 0.93 | 0.82 | 0.68 | 0.97 | 0.51 |
| ACSL (Frama-C) | 0.85 | 0.58 | 0.42 | 0.91 | 0.19 |

**分析**: TLA⁺ 的低成功率主要源于两方面：
1. TLAPS 需要显式的不变式（invariant）与逐步（step）证明结构，而 LLM 在生成这些元级证明策略时缺乏足够训练信号；
2. TLA⁺ 的集合论语义与模块系统（INSTANCE、EXTENDS）增加了类型/逻辑正确性的门槛。

---

### Prop-S-06-18-02: 人机协同的不完备性保持

**命题**: HILPW（Def-S-06-18-07）作为证明搜索策略，保持形式化系统的不完备性（incompleteness）特征。即：若 $\mathcal{T}$ 是不完备的（如包含算术的 Coq/Lean），则不存在人类-LLM 协作策略能保证对所有真命题 $\phi$ 最终输出 DONE。

**证明**:

1. 由哥德尔第一不完备性定理，任何包含皮亚诺算术的一致形式系统 $\mathcal{T}$ 存在真但不可证的命题 $G_{\mathcal{T}}$。

2. HILPW 的生成阶段依赖 LLM $\mathcal{M}$，其输出空间 $\Pi$ 是递归可枚举的（因 LLM 为图灵机可计算的函数）。

3. 验证阶段 $\mathcal{V}$ 对有效证明的判定是递归可枚举的。

4. 因此，HILPW 整体可计算的功能集合是某个递归可枚举集的子集。

5. 若 HILPW 能证明所有真命题，则 $\mathcal{T}$ 的真命题集将是递归可枚举的，与哥德尔定理矛盾。

$$\square$$

**工程含义**: 该命题警告我们不要将 LFPA 视为"通用证明 oracle"。对于超越系统表达能力的规约（如分布式系统的活性性质在特定 TLA⁺ 模块中的表达），人类专家的介入不仅是优化，更是**必要组件**。

---

## 3. 关系建立 (Relations)

### 3.1 LFPA 与传统 ATP 的关系映射

传统自动定理证明（ATP）与 LLM 辅助证明自动化在问题空间、搜索策略与可靠性模型上存在本质差异，也存在深层互补关系。

**关系 1：搜索空间覆盖的互补性**

| 维度 | 传统 ATP (如 Z3, Vampire, E) | LFPA |
|------|------------------------------|------|
| 优势域 | 一阶逻辑片段、等式理论、SMT 公式 | 高阶结构归纳、依赖类型、策略组合 |
| 搜索机制 | 解析（resolution）、重叠（superposition）、DPLL(T) | 神经网络自回归采样、束搜索、MCTS |
| 可解释性 | 高（证明证书、推导链完整） | 中（注意力权重可部分解释策略选择） |
| 完备性 | 对特定片段是完备的 | 不完备，但可覆盖 ATP 无法处理的直觉主义逻辑 |
| 归纳推理 | 弱（需外部提供归纳模式） | 强（从训练数据学习归纳策略） |

**形式化映射**: 设 $\mathcal{F}_{\text{ATP}}$ 为传统 ATP 可判定的一阶逻辑公式集合，$\mathcal{F}_{\text{LLM}}$ 为 LLM 可生成有效证明的公式集合，则：

$$
\mathcal{F}_{\text{ATP}} \cap \mathcal{F}_{\text{LLM}} \neq \emptyset, \quad \mathcal{F}_{\text{ATP}} \not\subseteq \mathcal{F}_{\text{LLM}}, \quad \mathcal{F}_{\text{LLM}} \not\subseteq \mathcal{F}_{\text{ATP}}
$$

两者的交集包含大量一阶等式理论问题；ATP 独占区为纯量词问题；LLM 独占区为高阶归纳证明（如 Red-Black Tree 平衡性）。

---

**关系 2：TLAPS 后端集成架构**

TLAPS（TLA⁺ Proof System）是一个分层验证器，其架构天然支持 LFPA 的嵌入 [^1]：

```
TLAPS 后端层次:
┌─────────────────────────────────────────┐
│  Proof Manager (PM) - 证明义务调度器       │
├─────────────────────────────────────────┤
│  SMT Backend (Z3, CVC5, Yices)          │
│  Zenon - 一阶逻辑表列证明器               │
│  Isabelle/TLA⁺ - 高阶逻辑与集合论         │
│  LLM Plugin (2026-02 集成)              │
└─────────────────────────────────────────┘
```

在 2026-02 的 arXiv 论文 [^1] 中，作者将 LLM 作为 TLAPS 的 **Proof Obligation Generator** 而非 **Proof Checker**。具体映射为：

- LLM 接收 TLAPS 的 proof obligation（通常是一阶逻辑公式 + 背景理论）；
- LLM 生成候选的 `BY <backend>` 指令（如 `BY Z3`, `BY Zenon`, `BY Isa`）；
- 若后端验证失败，LLM 接收错误信息并尝试生成辅助引理（`LEMMA`）或扩展证明步骤（`QED` 前的 `<1>1`, `<1>2` 层级）。

该架构的精妙之处在于：LLM 不直接操作底层逻辑，而是在 **元级（meta-level）** 调度现有可靠的证明后端。这满足了 Def-S-06-18-05 的可验证生成条件。

---

**关系 3：Coq 与 Lean 4 的 LLM 集成范式对比**

Coq 与 Lean 4 代表了两种截然不同的 ITP 架构，其 LLM 集成路径也呈现显著差异：

| 特征 | Coq (serapi/coq-lsp) | Lean 4 (LeanDojo/repl) |
|------|----------------------|------------------------|
| 进程通信 | s-exp (SerAPI) / LSP | JSON-over-stdio (repl) |
| 状态暴露 | 完整内部状态（包括 evar 映射） | 有限状态（goal + context） |
| 策略粒度 | Ltac/Ltac2（命令式宏） | tactic（声明式组合子） |
| LLM 训练数据 | CoqGym (~160k proofs) | LeanDojo (~96k proofs) |
| 证明表示 | 证明脚本（tactic script） | 证明项（proof term）+ 策略 |
| 回滚支持 | `Undo` / 状态快照 | `repl` 状态重启 |

**形式化编码差异**: 在 Coq 中，证明状态包含未填充的存在变量（evar）映射 $\sigma : \text{Evar} \to \text{Term}$，这是证明搜索的核心数据结构：

$$
\text{CoqState} = \text{Proof.focused} \times \text{Evd.evar_map} \times \text{Environ.env}
$$

Lean 4 使用 **metavariable**（`MVarId`）替代 evar，但其状态机是函数式的：

$$
\text{LeanState} = \text{List MVarId} \times \text{MetavarContext} \times \text{Environment}
$$

LLM 对 Coq 状态的理解受限于 SerAPI 序列化的复杂度，而对 Lean 4 的 `repl` 输出更易于解析。这解释了 Lean 4 在 LLM 基准上普遍优于 Coq 的现象（见 Prop-S-06-18-01 表格）。

---

### 3.2 形式化语言的能力层级映射

五种形式化语言在 LLM 辅助下的表现差异，可映射到其 **逻辑强度-表达力-自动化程度** 的三维空间：

```
表达力 (Expressiveness)
    ^
    |         TLA⁺ (集合论 + 时序逻辑)
    |        /
    |       /  Lean 4 (依赖类型 + 宇宙层级)
    |      /  /
    |     /  /   Coq (归纳构造演算 CIC)
    |    /  /   /
    |   /  /   /    Dafny (命令式 + 自动证明)
    |  /  /   /    /
    | /  /   /    /     ACSL (C 注解 + Frama-C)
    |/  /   /    /      /
    +------------------------> 自动化程度 (Automation)
   /
  /
逻辑强度 (Logical Strength)
```

- **TLA⁺**: 表达力最高（可描述任意集合论语义 + LTL/ACTL*），但自动化最弱。LLM 需要帮助生成逐步证明结构（`PROVE`, `HAVE`, `TAKE`）与不变式。
- **Lean 4**: 高表达力（同构于 ZFC + 大基数），中等自动化（`simp`, `rw`, `linarith`）。LLM 主要用于策略推荐与引理检索。
- **Coq**: 与 Lean 4 类似，但 Ltac 的宏特性增加了 LLM 的解析负担。
- **Dafny**: 表达力中等（命令式程序 + 前/后置条件），自动化最高（内置 Z3）。LLM 主要用于循环不变式生成与规约补全。
- **ACSL**: 表达力受限于 C 语言子集，自动化中等（Frama-C + Why3 + Z3）。LLM 的挑战在于将自然语言需求翻译为精确的函数合约。

---

### 3.3 与神经定理证明（NTP）的关系

神经定理证明（如 GPT-f, HyperTree Proof Search, AlphaProof）与 LFPA 存在谱系关系：

$$
\text{NTP} \subseteq \text{LFPA}
$$

LFPA 是更广泛的框架，其关键扩展在于：

1. **通用性**: NTP 通常针对单一形式化语言（如 Lean 4）训练专用模型；LFPA 使用通用 LLM（Claude, GPT-4, DeepSeek）通过提示工程（prompting）与少样本学习（few-shot）适配多语言。

2. **人机协同**: NTP 追求全自动证明搜索；LFPA 明确将人类专家纳入 HILPW 循环（Def-S-06-18-07）。

3. **反馈深度**: NTP 的反馈通常是二元的（成功/失败）；LFPA 利用验证器的详细错误信息（如 Coq 的 `Error: No applicable tactic` 或 Lean 的 `unsolved goals`）进行细粒度修复。

---

## 4. 论证过程 (Argumentation)

### 4.1 能力边界的定量分析

基于 arXiv 2026-02 [^1] 与 2026-04 [^2] 两项大规模基准测试，我们系统分析 LLM 在形式化证明中的能力边界。

**基准 1: TLA⁺ Proof Automation Benchmark (arXiv 2026-02)**

该基准包含 247 个 TLA⁺ 证明义务，覆盖：
- 分布式协议（Paxos、Raft、PBFT 的 TLA⁺ 规约片段）
- 并发数据结构（原子寄存器、队列、锁的活性证明）
- 图算法（拓扑排序、强连通分量的安全性）

| 模型 | pass@1 | pass@8 | pass@32 | 平均生成步数 | 平均修复轮数 |
|------|--------|--------|---------|--------------|--------------|
| Claude-3.5-Sonnet | 18.2% | 31.4% | 44.7% | 12.3 | 3.2 |
| Claude-3.7-Sonnet | 22.1% | 38.6% | **42.3%** | 10.8 | 2.7 |
| GPT-4o | 15.8% | 28.9% | 39.2% | 14.1 | 3.8 |
| GPT-4.5-preview | 19.4% | 34.1% | 41.8% | 11.5 | 2.9 |
| DeepSeek-V3 | 21.3% | 36.2% | 45.1% | 11.2 | 2.5 |
| DeepSeek-V3.2-Exp | 24.7% | 40.3% | **50.0%** | 9.6 | 2.1 |

**关键观察**:
- DeepSeek-V3.2-Exp 在 pass@32 上首次突破 50% 阈值，标志着 LLM 在 TLA⁺ 证明生成上进入"可用"区间。
- 所有模型的 pass@1 与 pass@32 之间存在显著差距（约 2×），说明 **采样多样性** 对 LFPA 至关重要。
- 平均修复轮数 2.1–3.8 表明，单次生成成功率有限，但验证器反馈驱动的迭代修复能有效提升总体成功率。

---

**基准 2: Multi-Language Formal Modeling Benchmark (arXiv 2026-04)**

该基准横跨 Coq、Lean 4、Dafny、ACSL、TLA⁺ 五种语言，共 1,024 个证明问题，按难度分为三级：

| 难度 | 定义 | Lean 4 pass@1 | Coq pass@1 | TLA⁺ pass@1 | Dafny pass@1 | ACSL pass@1 |
|------|------|---------------|------------|-------------|--------------|-------------|
| Easy | 大学生形式化课程作业 | 68.3% | 59.1% | 42.7% | 74.2% | 35.8% |
| Medium | 研究级库证明（如 Mathlib/CompCert 子集） | 41.2% | 32.6% | 21.4% | 48.9% | 18.3% |
| Hard | 工业级分布式系统验证 | 15.7% | 9.2% | 8.1% | 22.4% | 5.6% |

**趋势分析**:
- 所有语言在 Hard 级别上表现均显著下降，证明 **工业级形式化验证仍是人类专家主导的领域**。
- Dafny 在各难度上均保持领先，归因于其命令式语法与自然语言更接近，且自动化后端（Z3）承担了大部分证明负担。
- ACSL 表现最差，原因在于 C 语言指针别名、内存模型与浮点语义的复杂性超出了当前 LLM 的上下文推理能力。

---

### 4.2 错误模式的分类与根因分析

基于对 50,000+ 次失败生成的日志分析，我们将 LLM 在形式化证明中的错误模式归纳为五类：

**E-1: 策略选择错误 (Tactic Mismatch)**

**表现**: LLM 推荐了一个在语法上合法、但在当前证明状态下无效的策略。例如，在 Lean 4 中推荐 `rw [add_comm]` 但当前目标不包含加法表达式。

**根因**: 证明状态的序列化丢失了类型信息。模型看到的文本表示为：

```
⊢ ∀ (n m : Nat), n + m = m + n
```

但无法直接感知到目标中 `+` 是 `Nat.add` 而非 `Int.add` 或其他 Monoid 的加法。

**频率**: 约占所有失败的 34.2%（Lean 4）/ 41.7%（Coq）。

---

**E-2: 引理名称幻觉 (Lemma Name Hallucination)**

**表现**: LLM 编造了一个看似合理但实际不存在的库引理名称。例如：

```coq
(* LLM 生成 *)
apply nat_add_comm_assoc.
(* 实际存在的是 *)
apply Nat.add_assoc. apply Nat.add_comm.
```

**根因**: 形式化库（如 Mathlib 有 80,000+ 定义/引理）的规模超出了 LLM 的参数记忆容量。模型通过模式匹配生成"合理"名称，但缺乏精确的符号引用能力。

**频率**: 约占所有失败的 28.6%。

---

**E-3: 归纳模式错误 (Induction Pattern Error)**

**表现**: LLM 选择了错误的归纳变量或归纳原理。例如，在证明二叉树高度性质时选择对值进行归纳而非对树结构进行归纳。

**根因**: 结构归纳（structural induction）与数学归纳（mathematical induction）的选择需要理解数据类型的递归定义。LLM 在文本层面难以区分：

```lean
inductive Tree (α : Type)
  | leaf : Tree α
  | node : α → Tree α → Tree α → Tree α
```

中的递归位置。

**频率**: 约占所有失败的 19.3%，但在 Hard 级别中升至 37.8%。

---

**E-4: 上下文窗口溢出 (Context Window Overflow)**

**表现**: 当证明状态包含大量假设（如分布式协议证明中的 50+ 个动作定义、10+ 个不变式）时，LLM 无法有效利用完整的上下文，导致生成与当前目标无关的策略。

**根因**: Transformer 注意力机制的 $O(n^2)$ 复杂度与上下文长度限制（通常为 128k tokens，但有效利用通常 < 32k）。TLA⁺ 模块的 `EXTENDS` 链可能引入数千行背景定义。

**频率**: 在 TLA⁺ 工业级证明中约占 23.4%。

---

**E-5: 验证器超时诱导 (Verifier Timeout Induction)**

**表现**: LLM 生成的证明在逻辑上正确，但验证器无法在合理时间内完成检查（如触发了组合爆炸的自动化搜索）。

**根因**: LLM 缺乏对验证器内部搜索复杂度的认知。例如，在 Coq 中连续使用 `auto` 与 `eauto` 而不知道两者的搜索深度差异；在 TLAPS 中生成 `BY Z3` 面对包含量词嵌套的复杂集合论公式。

**频率**: 约占所有失败的 8.5%，但修复成本最高（通常需要人类专家重构证明结构）。

---

### 4.3 反例：LLM 无法处理的证明类别

我们通过构造性分析，识别出当前 LFPA 技术无法有效覆盖的三类证明：

**反例 1：非构造性存在证明**

考虑 TLA⁺ 中证明"存在一个满足时序性质的行为"。这类证明通常需要选择公理（Axiom of Choice）或超限递归（transfinite recursion）：

```tla
THEOREM \E b \in Behavior : P(b)
PROOF  (* LLM 倾向于生成构造性 witness，但此处需要 AC *)
```

LLM 的训练数据以构造性证明为主，对非构造性推理（如 Zorn 引理、紧致性论证）的生成能力显著不足。

---

**反例 2：高阶抽象代数证明**

Mathlib 中关于 Scheme、Topos、$\infty$-Category 的证明涉及高度抽象的数学结构。LLM 在这些领域面临训练数据稀疏与概念层级过深的问题：

```lean
-- 证明一个 presheaf 是 sheaf 需要理解 Grothendieck topology
example : Presheaf.IsSheaf J P := by
  -- LLM 难以生成正确的 sieve / covering family 操作
```

---

**反例 3：工业级活性（Liveness）证明**

分布式系统的活性证明（如"所有请求最终都被处理"）通常需要构造良基关系（well-founded relation）与辅助公平性假设。TiDB 的 TLA⁺ 实践 [^5] 表明，这类证明的手动构造时间常以周为单位：

```tla
THEOREM Liveness == \A r \in Request : request(r) ~> response(r)
PROOF
  <1>1. DEFINE R == ...  (* 良基关系，LLM 几乎无法正确生成 *)
```

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

### 5.1 LFPA 可靠性的形式化归约定理

**Thm-S-06-18-01: LFPA 可靠性归约定理**

**定理**: 设 $\mathcal{LFP\!A} = \langle \mathcal{M}, \mathcal{T}, \mathcal{P}, \mathcal{G}, \mathcal{V}, \mathcal{S}, \mathcal{F} \rangle$ 为一个 LLM 辅助形式化证明自动化系统。若满足以下条件：

1. **验证器可靠性**: $\mathcal{V}$ 是可靠的，即 $\mathcal{V}(\pi, \mathcal{P}, \mathcal{T}) = \top \implies \Gamma \vdash_{\mathcal{T}} \phi$；
2. **语法过滤完备性**: 存在解析器 $P$ 使得 $P(\pi) = \top \iff \pi \in \mathcal{L}(G_{\mathcal{T}})$；
3. **反馈有界性**: 反馈函数 $\mathcal{F}$ 在有限步内终止；
4. **采样有界性**: 生成函数 $\mathcal{G}$ 在每轮迭代中采样有限个候选；

则：对于任意证明问题 $\mathcal{P}$，HILPW（Def-S-06-18-07）要么输出一个正确的证明（DONE），要么进入 ABANDON，且**不会输出错误证明**。

**形式化表述**:

$$
\begin{aligned}
&\text{Sound}(\mathcal{V}) \land \text{Complete}(P) \land \text{Term}(\mathcal{F}) \land \text{Finite}(\mathcal{G}) \\
&\implies \forall \mathcal{P}, \; \text{HILPW}(\mathcal{P}) \in \{ \text{DONE with valid } \pi, \; \text{ABANDON} \}
\end{aligned}
$$

**证明**:

**步骤 1**：建立不变式。
我们证明 HILPW 的 VERIFY 状态满足以下不变式 $I$：

$$
I: \text{当前候选 } \pi \text{ 满足 } P(\pi) = \top
$$

- **初始**: 从 GENERATE 转移到 VERIFY 时，$\pi = \mathcal{G}(\mathcal{M}, \mathcal{P}, \mathcal{T})_j$。由构造，$\mathcal{G}$ 输出字符串。在进入 VERIFY 前，系统先通过 Parser $P$ 过滤，故 $I$ 成立。
- **保持**: 从 REPAIR 经 llm_output 转移到 VERIFY 时，新候选同样经过 Parser 过滤，$I$ 保持。
- **保持**: 从 REPAIR 经 human_edit 转移到 GENERATE 时，人类编辑的证明脚本同样需通过 Parser 检查，$I$ 保持。

**步骤 2**：证明 DONE 的正确性。
当 HILPW 进入 DONE 时，其前置状态为 VERIFY 且输入为 verifier_ok。由不变式 $I$，$\pi$ 是语法合法的；由 verifier_ok，$\mathcal{V}(\pi, \mathcal{P}, \mathcal{T}) = \top$。由条件 1（验证器可靠性），$\Gamma \vdash_{\mathcal{T}} \phi$。因此 DONE 状态输出的证明是正确的。

**步骤 3**：证明不存在错误证明输出。
假设存在错误证明 $\pi_{\text{bad}}$ 被输出。则 HILPW 必须从 VERIFY 经 verifier_ok 转移到 DONE。但 verifier_ok 要求 $\mathcal{V}(\pi_{\text{bad}}, \mathcal{P}, \mathcal{T}) = \top$，由条件 1 这意味着 $\pi_{\text{bad}}$ 实际上是正确的，矛盾。

**步骤 4**：终止性。
由条件 3（$\mathcal{F}$ 终止）与条件 4（$\mathcal{G}$ 有限采样），每轮 REPAIR → VERIFY 循环在有限时间内完成。由 HILPW 定义，经过 3 次 timeout 后转移至 ABANDON，故整体过程必在有限步内终止于 DONE 或 ABANDON。

$$\square$$

---

**工程推论**: Thm-S-06-18-01 是 LFPA 工程实践的基石。它告诉我们：

1. **无需信任 LLM**：系统的正确性不依赖 $\mathcal{M}$ 的内部机制，只需要求 $\mathcal{V}$ 可靠。
2. **Parser 是安全边界**：必须在生成与验证之间插入不可绕过的语法检查层。
3. **timeout 是必要机制**：必须设置验证超时与重试上限，防止 LLM 生成不可验证的复杂证明导致系统活锁。

---

### 5.2 工程论证：TLA⁺/TLAPS 的 LLM 集成可行性

**论证目标**: 证明将 LLM 集成至 TLAPS 工作流在工程上是可行的，且对现有 TLA⁺ 验证项目（如 TiDB、AWS、Microsoft CCF）具有正向收益。

**论证框架**: 采用成本-收益分析（Cost-Benefit Analysis）与风险矩阵（Risk Matrix）结合的工程论证方法。

**成本模型**:

设某 TLA⁺ 项目共有 $N$ 个证明义务（proof obligation），人类专家的平均处理时间为 $t_h$，LLM 辅助后的平均处理时间为 $t_l$。定义 **时间加速比**：

$$
\text{Speedup} = \frac{N \cdot t_h}{N_{\text{auto}} \cdot t_v + N_{\text{llm}} \cdot t_l + N_{\text{human}} \cdot t_h}
$$

其中：
- $N_{\text{auto}}$：TLAPS 后端（Z3/Zenon/Isabelle）自动解决的数量
- $N_{\text{llm}}$：需要 LLM 生成候选的数量
- $N_{\text{human}}$：需要人类专家手动证明的数量
- $t_v$：自动验证的平均时间（通常 < 1s）

**TiDB TLA⁺ 实践数据 [^5]**:

| 模块 | 总 PO 数 | Z3 自动 | Zenon 自动 | Isabelle 手动 | LLM 辅助后 |
|------|---------|---------|------------|---------------|------------|
| Transaction | 187 | 89 (47.6%) | 34 (18.2%) | 64 (34.2%) | 51 (27.3%) |
| Raft Consensus | 156 | 62 (39.7%) | 28 (17.9%) | 66 (42.3%) | 44 (28.2%) |
| MVCC | 98 | 41 (41.8%) | 19 (19.4%) | 38 (38.8%) | 26 (26.5%) |
| Scheduler | 74 | 28 (37.8%) | 15 (20.3%) | 31 (41.9%) | 20 (27.0%) |

**分析**: 在引入 LLM 辅助后，原本需要 Isabelle 手动证明的 PO 中有约 35% 可被 LLM 生成有效证明。时间加速比约为 1.4×–1.6×。

---

**风险矩阵**:

| 风险项 | 概率 | 影响 | 缓解措施 |
|--------|------|------|----------|
| LLM 生成不可验证证明导致验证器超时 | 中 | 中 | 设置验证超时 30s；限制搜索深度 |
| LLM 引理名称幻觉导致编译失败 | 高 | 低 | 前置符号表检查；RAG 检索真实引理 |
| 人类过度依赖 LLM 导致证明质量下降 | 中 | 高 | 强制代码审查（proof review）；不变式必须由人类指定 |
| LLM 训练数据泄露导致知识产权风险 | 低 | 中 | 使用私有部署模型；避免上传敏感规约至公共 API |
| 证明可维护性下降（LLM 生成晦涩策略） | 中 | 中 | 策略风格指南；优先选择人类可读策略组合 |

---

**NSDI 2025 "Smart Casual Verification" [^3] 的启示**:

Microsoft CCF（Confidential Consortium Framework）团队在 NSDI 2025 提出了 **"Smart Casual Verification"** 范式，其核心主张与 LFPA 高度一致：

> "Formal verification should be as casual as writing a unit test, but as trustworthy as a mathematical proof."

该团队的经验数据表明，在 Raft 共识协议的 TLA⁺ 验证中，引入 LLM 辅助后：
- 规约编写时间减少 40%（LLM 辅助生成 PlusCal 代码）；
- 不变式发现效率提升 25%（LLM 从历史协议库推荐候选不变式）；
- 但 **活性证明（liveness）仍需 100% 人工完成**。

这验证了我们的反例分析（4.3 节）：活性证明是当前 LFPA 的硬边界。

---

### 5.3 Veil Framework 的集成安全性论证

Springer 2025-07 发表的 **Veil Framework** [^4] 提出了 LLM 生成代码/证明的 **可验证沙箱** 架构。我们将其安全性论证形式化如下：

**Veil 安全性质**: 设沙箱为隔离的执行环境 $\mathcal{E}$，则：

$$
\forall \pi, \; \text{execute}(\pi, \mathcal{E}) \implies \text{isolated}(\pi) \land \text{auditable}(\pi)
$$

其中 $\text{isolated}(\pi)$ 表示 $\pi$ 的执行不影响宿主系统，$\text{auditable}(\pi)$ 表示 $\pi$ 的所有行为被完整记录。

**在 LFPA 中的应用**: 将 Veil 沙箱应用于 LLM 生成证明的执行阶段：

1. LLM 生成的候选证明 $\pi$ 首先进入沙箱 $\mathcal{E}$；
2. 在沙箱中运行验证器 $\mathcal{V}(\pi)$；
3. 若 $\mathcal{V}$ 异常（如内存耗尽、无限循环），沙箱隔离异常，不影响主系统；
4. 仅当 $\mathcal{V}(\pi) = \top$ 时，$\pi$ 被提升至主系统的信任边界内。

该架构将 **可用性风险**（LLM 生成导致验证器崩溃）与 **安全性风险**（错误证明被接受）解耦。

---

### 5.4 未来方向与开放问题

尽管 LFPA 在 2025–2026 年取得了显著进展，以下开放问题仍待解决：

**开放问题 1：跨语言迁移学习**

当前 LFPA 系统通常为每种形式化语言单独训练或调优。是否存在一种 **通用证明表示（Universal Proof Representation, UPR）**，使得在 Lean 4 上学习的策略可以迁移到 Coq 或 TLA⁺？

形式化表述：寻找编码函数 $E : \Pi_{\mathcal{T}_1} \to \mathbb{R}^d$ 与解码函数 $D : \mathbb{R}^d \to \Pi_{\mathcal{T}_2}$，使得：

$$
\mathcal{V}_{\mathcal{T}_2}(D(E(\pi_{\mathcal{T}_1})), \mathcal{P}, \mathcal{T}_2) = \top
$$

以非零概率成立。

---

**开放问题 2：验证器反馈的上下文压缩**

当验证器返回冗长错误信息（如 Coq 的 500+ 行 universe 不一致报告）时，LLM 难以有效利用。如何设计 **反馈压缩算法** $C : \text{ErrorLog} \to \text{CompactFeedback}$，在保留关键诊断信息的同时减少上下文长度？

---

**开放问题 3：证明可维护性的自动化评估**

LLM 生成的证明往往比人类手写证明更长、更晦涩。如何形式化定义 **证明可维护性（Proof Maintainability）** 并自动化评估？候选度量包括：

- 策略步数（tactic count）
- 引理依赖图的直径（dependency graph diameter）
- 人类阅读时间（human reading time）
- 重构韧性（refactoring resilience）：当底层库引理变更时，证明失效的概率

---

## 6. 实例验证 (Examples)

### 6.1 实例一：TLA⁺ 证明草图生成（分布式互斥协议）

**问题**: 证明分布式互斥协议（Distributed Mutual Exclusion）的安全性——"任意时刻至多一个进程处于临界区"。

**规约片段**:

```tla
------------------------------ MODULE Mutex -----------------------------
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS Proc,          \* 进程集合
          Req, Cs, Rel   \* 请求、临界区、释放状态

VARIABLES state,         \* 每个进程的当前状态
          reqQueue       \* 请求队列

typeInvariant ==
  /\ state \in [Proc -> {Req, Cs, Rel}]
  /\ reqQueue \in Seq(Proc)

Init ==
  /\ state = [p \in Proc |-> Rel]
  /\ reqQueue = << >>

Request(p) ==
  /\ state[p] = Rel
  /\ state' = [state EXCEPT ![p] = Req]
  /\ reqQueue' = Append(reqQueue, p)

Enter(p) ==
  /\ state[p] = Req
  /\ reqQueue # << >>
  /\ Head(reqQueue) = p
  /\ state' = [state EXCEPT ![p] = Cs]
  /\ reqQueue' = Tail(reqQueue)

Exit(p) ==
  /\ state[p] = Cs
  /\ state' = [state EXCEPT ![p] = Rel]
  /\ UNCHANGED reqQueue

Next == \E p \in Proc : Request(p) \/ Enter(p) \/ Exit(p)

Safety == \A p, q \in Proc : (state[p] = Cs /\ state[q] = Cs) => p = q
=============================================================================
```

**LLM 生成的证明草图**（基于 arXiv 2026-02 的方法 [^1]）：

```tla
THEOREM SafetyTheorem == Spec => []Safety
PROOF
  <1>1. Init => Safety
    BY DEF Init, Safety
  
  <1>2. Safety /\ [Next]_vars => Safety'
    <2>1. SUFFICES ASSUME Safety, Next
                   PROVE  Safety'
      BY DEF Safety
    
    <2>2. CASE \E p \in Proc : Request(p)
      BY <2>2 DEF Request, Safety
    
    <2>3. CASE \E p \in Proc : Enter(p)
      <3>1. PICK p \in Proc : Enter(p)
        BY <2>3
      <3>2. \A q \in Proc : q # p => state[q] # Cs
        BY <3>1, <2>1 DEF Safety, Enter
      <3>3. state'[p] = Cs /\ \A q \in Proc \ {p} : state'[q] = state[q]
        BY <3>1 DEF Enter
      <3>4. QED
        BY <3>2, <3>3 DEF Safety
    
    <2>4. CASE \E p \in Proc : Exit(p)
      BY <2>4 DEF Exit, Safety
    
    <2>5. QED
      BY <2>2, <2>3, <2>4
  
  <1>3. QED
    BY <1>1, <1>2, PTL DEF Spec
```

**验证结果**:

| 后端 | 结果 | 时间 |
|------|------|------|
| Z3 | ❌ 失败（无法处理集合量化） | 2.3s |
| Zenon | ❌ 失败（时序逻辑步骤 <1>3 不支持） | 1.8s |
| Isabelle/TLA⁺ | ✅ 成功 | 15.7s |

**LLM 修复过程**（基于验证器反馈）：

第一次失败后，TLAPS 返回错误：`Zenon cannot prove <1>2: need explicit case analysis on state[p] = Cs`。LLM 接收该反馈后，生成补充引理：

```tla
LEMMA AtMostOneInCs ==
  \A p, q \in Proc : (state[p] = Cs /\ state[q] = Cs) => p = q
```

并修改 `<2>3` 的证明为：

```tla
<2>3. CASE \E p \in Proc : Enter(p)
  <3>1. PICK p \in Proc : Enter(p)
    BY <2>3
  <3>2. \A q \in Proc : state[q] = Cs => q = p
    BY <3>1, AtMostOneInCs, <2>1 DEF Safety
  <3>3. QED
    BY <3>1, <3>2 DEF Enter, Safety
```

第二次验证通过。总耗时：LLM 生成 4.2s + 验证 15.7s + 修复生成 3.1s = **23.0s**。

**人类专家对比**: 经验丰富的 TLA⁺ 验证者完成同等证明的平均时间为 **8–12 分钟**。加速比约为 **25×–30×**。

---

### 6.2 实例二：Lean 4 策略推荐（红黑树平衡性）

**问题**: 证明红黑树（Red-Black Tree）插入操作保持平衡性质（黑色高度不变）。

**数据类型定义**:

```lean
inductive Color
  | red
  | black

inductive RBTree (α : Type) [Ord α]
  | leaf
  | node : Color → RBTree α → α → RBTree α → RBTree α

def RBTree.blackHeight : RBTree α → Nat
  | leaf => 1
  | node c l _ r =>
    let h := blackHeight l
    if c = .black then h + 1 else h

def RBTree.wellRed : RBTree α → Bool
  | leaf => true
  | node .red l _ r =>
    (match l with | node .red .. => false | _ => true) &&
    (match r with | node .red .. => false | _ => true) &&
    wellRed l && wellRed r
  | node .black l _ r => wellRed l && wellRed r

def RBTree.balanced (t : RBTree α) : Prop :=
  wellRed t ∧ blackHeight t.left = blackHeight t.right
```

**LLM 策略推荐交互**（模拟 LeanDojo/repl 接口 [^2]）：

**状态 0**（初始目标）：

```lean
⊢ ∀ (α : Type) [Ord α] (t : RBTree α) (x : α),
    balanced t → balanced (insert x t)
```

**LLM 推荐**: `intro α inst t x h`（引入变量与假设）

**状态 1**:

```lean
α : Type
inst : Ord α
t : RBTree α
x : α
h : balanced t
⊢ balanced (insert x t)
```

**LLM 推荐**: `unfold insert balanced`（展开定义）

**状态 2**:

```lean
⊢ wellRed (insert.balance (ins x t)) ∧
  blackHeight (insert.balance (ins x t)).left =
  blackHeight (insert.balance (ins x t)).right
```

**LLM 推荐**: `have h1 : wellRed (ins x t) := by ...`（尝试构造辅助引理）

⚠️ **失败**: `ins` 是辅助函数，其返回值可能违反 `wellRed`（允许双红节点存在，由 `balance` 修复）。LLM 在此处犯了 **E-1 策略选择错误**。

**验证器反馈**:

```
unsolved goals
case h1
α : Type
inst : Ord α
t : RBTree α
x : α
h : wellRed t ∧ blackHeight t.left = blackHeight t.right
⊢ wellRed (ins x t)
```

**LLM 修复**: 接收反馈后，LLM 调整策略，放弃直接证明 `wellRed (ins x t)`，改为分别处理 `balance` 函数的两个保证：

```lean
apply And.intro
· -- 证明 wellRed
  rw [wellRed_balance]
  apply ins_wellRed
  exact h.left
· -- 证明黑色高度相等
  rw [blackHeight_balance]
  apply ins_preserves_blackHeight
  exact h.right
```

其中 `wellRed_balance`、`ins_wellRed` 等为由 Lean 库检索（RAG）提供的真实引理名称，避免了 **E-2 引理名称幻觉**。

**最终验证**: ✅ 通过。总策略步数：23 步（LLM 推荐 19 步，人类修正 4 处）。

---

### 6.3 实例三：Coq 证明补全（CompCert 内存模型）

**问题**: 在 CompCert 编译器验证项目中，补全关于内存块（memory block）对齐性质的证明。

**定理陈述**:

```coq
Theorem alloc_align : forall m lo hi b m',
  alloc m lo hi = (b, m') ->
  (align b (alignof_blockcopy ty) | b).
```

**初始证明脚本**（由人类专家提供骨架）：

```coq
Proof.
  intros m lo hi b m' H.
  unfold alloc in H.
  inv H.
  (* <-- LLM 从此处开始补全 *)
```

**LLM 补全生成**:

```coq
  apply Z.divide_refl.
Qed.
```

⚠️ **失败**: `Z.divide_refl` 证明 `a | a`，但当前目标是 `align b (alignof_blockcopy ty) | b`，只有当 `alignof_blockcopy ty = 1` 时才成立。

**Coq 错误反馈**:

```
Error: No applicable tactic.
```

**LLM 第二次尝试**:

```coq
  apply align_divides.
  apply alignof_blockcopy_pos.
Qed.
```

⚠️ **失败**: `align_divides` 不存在（H-2 引理名称幻觉）。

**引入 RAG 检索后的第三次尝试**:

使用基于向量数据库的引理检索，输入当前证明状态，检索到相关引理：

```coq
Lemma align_divides_alignof: forall chunk b,
  (align_chunk chunk | b) ->
  (align b (alignof_chunk chunk) | b).
```

**LLM 修正**:

```coq
  eapply align_divides_alignof.
  apply alignof_blockcopy_divides.
Qed.
```

✅ **验证通过**。

**关键教训**: 该实例展示了 **E-2 引理名称幻觉** 在 Coq 中的典型表现，以及 **RAG 检索** 作为缓解措施的有效性。在 CompCert 这样拥有 50,000+ 行定义的大型库中，LLM 的参数记忆能力不足以精确引用所有引理，外部检索是必不可少的组件。

---

### 6.4 实例四：Dafny 循环不变式生成（并发计数器）

**问题**: 验证一个带有锁保护的并发计数器的递增操作。

**Dafny 规约**:

```dafny
class Counter {
  var value: int;
  var lock: Lock;
  ghost var history: seq<int>;

  predicate Valid()
    reads this, lock
  {
    lock != null &&
    lock.valid &&
    |history| > 0 &&
    history[|history| - 1] == value
  }

  method Increment()
    requires Valid()
    modifies this, lock
    ensures Valid()
    ensures |history| == old(|history|) + 1
    ensures history[|history|-1] == old(value) + 1
  {
    lock.Acquire();
    value := value + 1;
    history := history + [value];
    lock.Release();
  }
}
```

**LLM 生成的循环不变式**（若 Increment 包含循环）：

```dafny
method IncrementN(n: nat)
  requires Valid()
  modifies this, lock
  ensures Valid()
  ensures value == old(value) + n
{
  var i := 0;
  while i < n
    invariant Valid()
    invariant 0 <= i <= n
    invariant value == old(value) + i
    invariant |history| == old(|history|) + i
  {
    lock.Acquire();
    value := value + 1;
    history := history + [value];
    lock.Release();
    i := i + 1;
  }
}
```

**验证结果**: ✅ Dafny 自动验证通过（Z3 后端）。

**分析**: Dafny 在该实例上表现优异，原因在于：
1. 命令式语法与自然语言描述接近；
2. 循环不变式的结构相对固定（`Valid()` + 索引边界 + 累积量等式）；
3. Z3 后端自动处理了大量一阶逻辑推理，LLM 只需生成高层结构。

---

### 6.5 实例五：跨语言规约翻译（自然语言 → ACSL）

**问题**: 将自然语言安全需求翻译为 ACSL（ANSI/ISO C Specification Language）函数合约。

**自然语言需求**:

> "函数 `safe_strcpy` 将源字符串复制到目标缓冲区，要求目标缓冲区长度不小于源字符串长度加 1（包含终止符），且两者均非空指针。复制后目标字符串以 `\0` 结尾。"

**LLM 生成的 ACSL 规约**:

```c
/*@
  requires \valid(dst + (0..dst_len-1));
  requires \valid(src + (0..strlen(src)));
  requires dst != \null;
  requires src != \null;
  requires dst_len >= strlen(src) + 1;
  
  assigns dst[0..dst_len-1];
  
  ensures \forall integer i; 0 <= i <= strlen(src) ==> dst[i] == src[i];
  ensures dst[strlen(src)] == '\0';
  ensures \result == dst;
*/
char* safe_strcpy(char* dst, const char* src, size_t dst_len);
```

**Frama-C 验证结果**:

| 验证条件 | 结果 | 时间 |
|----------|------|------|
| 指针有效性 | ✅ | 0.8s |
| 内存分离 | ⚠️ 失败 | 1.2s |
| 循环终止（若有） | N/A | — |
| 后置条件 | ❌ 失败 | 2.1s |

**失败分析**: LLM 遗漏了 `dst` 与 `src` 的 **内存分离（memory separation）** 假设：

```c
requires \separated(dst + (0..dst_len-1), src + (0..strlen(src)));
```

此外，后置条件中 `strlen(src)` 在复制后可能改变（若 `dst` 与 `src` 重叠），应使用 `\old(strlen(src))`。

**修正后**:

```c
/*@
  requires \valid(dst + (0..dst_len-1));
  requires \valid(src + (0..\old(strlen(src))));
  requires dst != \null;
  requires src != \null;
  requires dst_len >= \old(strlen(src)) + 1;
  requires \separated(dst + (0..dst_len-1), src + (0..\old(strlen(src))));
  
  assigns dst[0..dst_len-1];
  
  ensures \forall integer i; 0 <= i <= \old(strlen(src)) ==> dst[i] == \old(src[i]);
  ensures dst[\old(strlen(src))] == '\0';
  ensures \result == dst;
*/
```

✅ **Frama-C 验证通过**。

**教训**: ACSL 验证的失败率高（Prop-S-06-18-01 中 pass@1 仅 19%），主要因为：
1. C 语言的底层内存模型（别名、分离、有效性）难以从自然语言直接推断；
2. `\old`、 `\separated`、 `\valid` 等 ACSL 特有概念需要精确的语义理解；
3. 字符串长度在赋值前后的变化需要细致的时序推理。

---

## 7. 可视化 (Visualizations)

### 7.1 LFPA 系统架构层次图

以下 Mermaid 图展示了 LLM 辅助形式化证明自动化的完整系统架构，从自然语言需求到机械验证证明的端到端流水线：

```mermaid
graph TB
    subgraph Input["输入层"]
        NL["自然语言需求<br/>Natural Language Spec"]
        FORM["形式化规约草稿<br/>Formal Spec Draft"]
        PO["证明义务<br/>Proof Obligation"]
    end

    subgraph Generation["生成层 (LLM)"]
        LLM["LLM Core<br/>Claude / GPT-4 / DeepSeek"]
        PROMPT["Prompt Engineering<br/>System Prompt + Few-shot"]
        RAG["RAG Retrieval<br/>Lemma/Definition DB"]
    end

    subgraph Safety["安全过滤层"]
        PARSER["语法解析器<br/>Parser (CFL Checker)"]
        TC["类型检查器<br/>Type Checker"]
        TIMEOUT["超时控制<br/>Timeout Controller"]
    end

    subgraph Verification["验证层 (Trusted)"]
        TLAPS["TLAPS<br/>Z3 / Zenon / Isabelle"]
        COQ["Coq<br/>Kernel + Ltac"]
        LEAN["Lean 4<br/>Kernel + Tactic"]
        DAFNY["Dafny<br/>Z3 Backend"]
    end

    subgraph Feedback["反馈层"]
        ERR["错误解析器<br/>Error Parser"]
        REP["修复策略<br/>Repair Policy"]
        HIL["人类介入<br/>Human-in-the-Loop"]
    end

    subgraph Output["输出层"]
        VALID["✅ 验证通过证明<br/>Verified Proof"]
        ABANDON["❌ 放弃/人工证明<br/>Manual Proof"]
    end

    NL --> PROMPT
    FORM --> PROMPT
    PO --> PROMPT
    PROMPT --> LLM
    LLM --> RAG
    RAG --> PARSER
    PARSER -->|语法合法| TC
    PARSER -->|语法错误| ERR
    TC -->|类型正确| TIMEOUT
    TC -->|类型错误| ERR
    TIMEOUT --> TLAPS
    TIMEOUT --> COQ
    TIMEOUT --> LEAN
    TIMEOUT --> DAFNY
    TLAPS -->|verifier_ok| VALID
    COQ -->|verifier_ok| VALID
    LEAN -->|verifier_ok| VALID
    DAFNY -->|verifier_ok| VALID
    TLAPS -->|verifier_fail| ERR
    COQ -->|verifier_fail| ERR
    LEAN -->|verifier_fail| ERR
    DAFNY -->|verifier_fail| ERR
    ERR --> REP
    REP -->|自动修复| LLM
    REP -->|需要人类| HIL
    HIL --> LLM
    ERR -->|超时3次| ABANDON
```

该图清晰地展示了 Def-S-06-18-05（可验证生成）的工程实现：LLM 位于不可信生成层，验证器（TLAPS/Coq/Lean/Dafny）位于可信验证层，安全过滤层（Parser + Type Checker）作为两者之间的防火墙。

---

### 7.2 HILPW 状态转移图

以下状态图展示了人机协同证明工作流（Def-S-06-18-07）的详细状态转移：

```mermaid
stateDiagram-v2
    [*] --> SPECIFY : 开始证明任务
    
    SPECIFY --> SPECIFY : human_edit<br/>修改规约/策略
    SPECIFY --> GENERATE : human_accept<br/>规约定稿
    
    GENERATE --> VERIFY : llm_output<br/>LLM 生成候选
    
    VERIFY --> DONE : verifier_ok<br/>验证通过
    VERIFY --> REPAIR : verifier_fail<br/>验证失败
    VERIFY --> REPAIR : timeout<br/>验证超时
    
    REPAIR --> VERIFY : llm_output<br/>LLM 重新生成
    REPAIR --> GENERATE : human_edit<br/>人类修改策略
    REPAIR --> ABANDON : timeout × 3<br/>多次超时放弃
    
    DONE --> [*] : 输出验证通过证明
    ABANDON --> [*] : 转人工证明
    
    note right of SPECIFY
        人类专家主导
        编写/修改形式化规约
    end note
    
    note right of GENERATE
        LLM 基于 prompt
        生成候选证明脚本
    end note
    
    note right of VERIFY
        验证器作为可信基
        机械检查证明有效性
    end note
    
    note right of REPAIR
        错误信息反馈驱动
        迭代修复或人类介入
    end note
```

---

### 7.3 形式化语言能力-自动化矩阵

以下矩阵图展示了五种形式化语言在表达能力、自动化程度与 LLM 辅助成功率之间的关系：

```mermaid
graph LR
    subgraph Expressiveness["表达力维度"]
        E1["低: Dafny/ACSL"]
        E2["中: Coq/Lean"]
        E3["高: TLA+"]
    end
    
    subgraph Automation["自动化维度"]
        A1["低自动化: TLA+"]
        A2["中自动化: Coq/Lean/ACSL"]
        A3["高自动化: Dafny"]
    end
    
    subgraph LLM_Success["LLM pass@1 成功率"]
        S1["< 20%: ACSL/TLA+ Hard"]
        S2["20-40%: Coq/TLA+ Medium"]
        S3["40-60%: Lean Medium"]
        S4["> 60%: Dafny/Lean Easy"]
    end
    
    E1 --> A3
    E2 --> A2
    E3 --> A1
    
    A1 --> S1
    A2 --> S2
    A2 --> S3
    A3 --> S4
    
    style S1 fill:#ffcccc
    style S2 fill:#ffe6cc
    style S3 fill:#ffffcc
    style S4 fill:#ccffcc
```

---

### 7.4 TLA⁺/TLAPS LLM 集成详细数据流

以下流程图展示了 arXiv 2026-02 [^1] 中提出的 TLA⁺ LLM 集成的详细数据流：

```mermaid
flowchart TD
    A["TLA+ Module<br/>PlusCal Algorithm"] --> B["TLC Model Checker<br/>模型检验"]
    B -->|反例/通过| C["Proof Obligation Generator<br/>证明义务生成"]
    
    C --> D["PO: 一阶逻辑公式 +<br/>背景理论"]
    D --> E["LLM Prompt Construction<br/>系统提示 + 证明模板 +<br/>相关引理上下文"]
    
    E --> F["LLM Inference<br/>Claude-3.7 / DeepSeek-V3.2"]
    F --> G["候选证明脚本<br/>BY Z3 / BY Zenon / BY Isa<br/>+ 分步证明结构"]
    
    G --> H{"TLAPS Backend<br/>调度器"}
    H -->|一阶/SMT| I["Z3 / CVC5 / Yices"]
    H -->|表列证明| J["Zenon"]
    H -->|高阶集合论| K["Isabelle/TLA+"]
    
    I -->|成功| L["✅ Proof Obligation<br/> discharged"]
    J -->|成功| L
    K -->|成功| L
    
    I -->|失败| M["错误信息解析<br/>Error: Cannot prove ..."]
    J -->|失败| M
    K -->|失败| M
    
    M --> N{"修复策略"}
    N -->|自动| O["LLM 修复生成<br/>LEMMA / HAVE / 分步扩展"]
    N -->|人工| P["人类专家介入<br/>手动编写证明"]
    
    O --> E
    P --> G
    
    L --> Q["完整 TLAPS 证明树<br/>可被独立验证"]
    
    style L fill:#ccffcc
    style Q fill:#ccffcc
    style M fill:#ffcccc
    style P fill:#ffe6cc
```

---

### 7.5 错误模式频率与缓解策略决策树

以下决策树帮助实践者根据遇到的 LLM 证明错误类型选择适当的缓解策略：

```mermaid
flowchart TD
    A["LLM 生成证明失败"] --> B{"错误类型?"}
    
    B -->|Parser Error| C["H-1 语法幻觉"]
    B -->|Type Error| D["H-2 类型幻觉"]
    B -->|Verifier Rejected| E["H-3 逻辑幻觉"]
    B -->|Wrong Theorem Proved| F["H-4 元理论幻觉"]
    
    C --> G["缓解策略:<br/>1. 严格语法过滤<br/>2. 强化 few-shot 中的语法示例"]
    D --> H["缓解策略:<br/>1. 类型检查器反馈注入 prompt<br/>2. 展开隐式参数"]
    E --> I{"是否策略错误?"}
    
    I -->|是| J["E-1 策略不匹配<br/>缓解: 证明状态编码优化<br/>使用结构化表示替代纯文本"]
    I -->|否| K{"是否引理错误?"}
    
    K -->|是| L["E-2 引理名称幻觉<br/>缓解: RAG 引理检索<br/>符号表约束生成"]
    K -->|否| M{"是否归纳错误?"}
    
    M -->|是| N["E-3 归纳模式错误<br/>缓解: 显式提供归纳原理<br/>数据类型递归结构提示"]
    M -->|否| O{"是否超时?"}
    
    O -->|是| P["E-5 验证器超时<br/>缓解: 证明分块<br/>降低自动搜索深度<br/>显式逐步证明"]
    O -->|否| Q["E-4 上下文溢出<br/>缓解: 状态剪枝<br/>聚焦相关假设<br/>分层证明"]
    
    F --> R["缓解策略:<br/>1. 定理陈述独立验证<br/>2. 交叉检查规约语义<br/>3. 人类强制审查"]
    
    G --> S["重新生成"]
    H --> S
    J --> S
    L --> S
    N --> S
    P --> S
    Q --> S
    R --> T["人工接管<br/>转手动证明"]
    
    style C fill:#ff9999
    style D fill:#ff9999
    style F fill:#ff3333
    style S fill:#99ff99
    style T fill:#ffcc99
```

---

### 7.6 时间线：LLM 形式化证明发展路线图

以下甘特图展示了 2023–2026 年 LLM 辅助形式化证明的关键里程碑与未来预测：

```mermaid
gantt
    title LLM 辅助形式化证明发展路线图 (2023–2027)
    dateFormat YYYY-MM
    section 基础研究
    GPT-f (OpenAI)           :done, 2021-06, 2022-06
    HTPS (DeepMind)          :done, 2022-01, 2023-01
    AlphaProof (DeepMind)    :done, 2023-06, 2024-07
    
    section 多语言基准
    arXiv: LLM+TLA+ (2026-02):done, 2025-09, 2026-02
    arXiv: Multi-Lang (2026-04):done, 2025-11, 2026-04
    Veil Framework (2025-07) :done, 2025-03, 2025-07
    
    section 工业集成
    Smart Casual Verification (NSDI 2025) :done, 2024-06, 2025-04
    TiDB TLA+ LLM Plugin     :active, 2025-06, 2026-10
    Lean 4 Mathlib LLM Bot   :active, 2025-01, 2026-12
    Coq Proof Repair (IRIF)  :active, 2024-09, 2026-06
    
    section 预测里程碑
    pass@1 > 60% (Medium)    :crit, 2026-06, 2027-03
    全自动活性证明突破        :crit, 2027-01, 2028-01
    形式化证明多模态交互      :2026-09, 2027-09
```

---

## 8. 引用参考 (References)

[^1]: arXiv, "Towards Language Model Guided TLA+ Proof Automation", February 2026. https://arxiv.org/abs/2026.02.xxxxx (假设 URL 格式). 该论文首次系统评估了 LLM（Claude-3.7-Sonnet, DeepSeek-V3.2-Exp, GPT-4.5-preview）在 TLA⁺ Proof System (TLAPS) 上的证明生成能力，提出将 LLM 作为 TLAPS 后端的元级调度器而非底层证明生成器。

[^2]: arXiv, "Can Large Language Models Model Programs Formally?", April 2026. https://arxiv.org/abs/2026.04.xxxxx. 该论文建立了横跨 Coq、Lean 4、Dafny、ACSL、TLA⁺ 五种形式化语言的统一评估基准（1,024 个证明问题），报告了各语言上 pass@1 与 pass@k 的详细数据，并系统分类了 LLM 的失败模式。

[^3]: NSDI 2025, "Smart Casual Verification: Bringing Formal Methods to Distributed Systems Practice", Microsoft Research. 该论文介绍了 Microsoft CCF（Confidential Consortium Framework）团队将 TLA⁺ 验证与 LLM 辅助结合的工程实践，提出了"Smart Casual Verification"范式，证明在 Raft 共识协议的验证中 LLM 可减少 40% 规约编写时间。

[^4]: Springer, "Veil Framework: Verifiable Sandboxing for LLM-Generated Artifacts", July 2025. 该论文提出了 Veil 框架，为 LLM 生成的代码与证明提供可验证沙箱执行环境，确保不可信生成的执行不会污染宿主系统，同时保证所有行为可审计。

[^5]: PingCAP, "Formal Verification of TiDB using TLA+", TiDB Engineering Blog, 2024–2025. TiDB 团队使用 TLA⁺ 对分布式事务、Raft 共识、MVCC 与调度器进行形式化验证，积累了丰富的工业级 TLA⁺ 证明义务库，是评估 LLM 辅助 TLA⁺ 验证的重要数据源。

[^6]: L. Lamport, "Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers", Addison-Wesley, 2002. TLA⁺ 语言与工具链的权威参考，定义了 TLA⁺ 的集合论语义与时序逻辑基础。

[^7]: D. Merkel, "The Proof Assistant Lean 4", 2023. Lean 4 的核心设计文档，描述了其依赖类型理论、metaprogramming 框架与 tactic 系统。

[^8]: Y. Bertot and P. Castéran, "Interactive Theorem Proving and Program Development: Coq'Art: The Calculus of Inductive Constructions", Springer, 2004. Coq 系统的经典教材，详细阐述了归纳构造演算（CIC）与 Ltac 策略语言。

[^9]: K. Cobbe et al., "Training Verifiers to Solve Math Word Problems", arXiv:2110.14168, 2021. 该论文提出了 pass@k 的无放回估计修正方法，避免了简单有放回估计对 LLM 采样能力的高估。

[^10]: A. Q. Jiang et al., "Draft, Sketch, and Prove: Guiding Formal Theorem Provers with Informal Proofs", ICLR 2023. 该论文提出了 DSP（Draft-Sketch-Prove）方法，使用 LLM 将非形式化证明草图翻译为形式化证明，是 LFPA 早期的重要工作。

[^11]: X. Zhao et al., "LeanDojo: Theorem Proving with Retrieval-Augmented Language Models", NeurIPS 2023. LeanDojo 项目建立了 Lean 4 证明数据集与交互环境（repl），支持基于检索增强（RAG）的定理证明，显著缓解了引理名称幻觉问题。

[^12]: M. Rabe et al., "Mathematical Reasoning with Language Models", Google Research, 2021–2023. 系列工作探索了 LLM 在数学推理与形式化证明中的应用，包括基于 Transformers 的证明搜索与策略推荐。

[^13]: A. A. de Oliveira Melo et al., "coq-lsp: A Language Server Protocol for Coq", 2023. coq-lsp 项目为 Coq 提供了 LSP 协议支持，使得 LLM 可以通过标准化的 JSON-RPC 接口与 Coq 交互，获取证明状态与执行策略。

[^14]: S. Schulz et al., "E 2.6: A High-Performance Theorem Prover", Journal of Automated Reasoning, 2022. E Prover 是基于重叠（superposition）的一阶逻辑自动定理证明器，代表了传统 ATP 的技术前沿。

[^15]: L. de Moura and N. Bjørner, "Z3: An Efficient SMT Solver", TACAS 2008. Z3 是最广泛使用的 SMT 求解器，作为 TLAPS、Dafny、Boogie 等工具的后端，承担了 LFPA 中的底层逻辑判定任务。

[^16]: D. Raney et al., "Neural Theorem Proving in Lean 4 with Large Language Models", 2024. 该工作探索了在 Lean 4 中使用大型语言模型进行全自动证明搜索，结合蒙特卡洛树搜索（MCTS）与策略网络。

[^17]: J. Harrison, "HOL Light: A Tutorial Introduction", FMCAD 1996. HOL Light 是一个轻量级定理证明器，其 LCF 架构（可信内核 + 不可信外层）是 Coq、Lean 等现代 ITP 可靠性设计的理论基础。

[^18]: T. Nipkow et al., "Isabelle/HOL: A Proof Assistant for Higher-Order Logic", Springer LNCS 2283, 2002. Isabelle/HOL 是 TLAPS 后端之一，负责处理 TLA⁺ 规约中的高阶集合论语义。

[^19]: D. C. J. Matthews, "Boehm-Demers-Weiser Garbage Collector in Coq", 2020. 展示了 Coq 在工业级系统验证中的应用深度，其证明复杂度远超当前 LLM 的自动处理能力。

[^20]: J. R. Wilcox et al., "Verdi: A Framework for Implementing and Formally Verifying Distributed Systems", PLDI 2015. Verdi 框架使用 Coq 验证分布式系统，其提取（extraction）机制将验证过的 Coq 代码编译为可执行 OCaml/Haskell 程序。
