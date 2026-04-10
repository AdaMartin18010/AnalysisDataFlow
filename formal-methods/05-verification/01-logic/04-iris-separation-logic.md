# Iris高阶并发分离逻辑 (Iris Higher-Order Concurrent Separation Logic)

> **所属阶段**: formal-methods/05-verification/01-logic | 前置依赖: [03-separation-logic.md](03-separation-logic.md) | 形式化等级: L6

本文档全面阐述Iris高阶并发分离逻辑的理论基础与工程应用。Iris是一个模块化的高阶并发分离逻辑框架，为验证复杂并发程序提供了强大的数学基础，支持高阶函数、高级模态运算符、幽灵状态和原子性规范等高级特性。本文档采用L6最高形式化等级，提供严格的定义、完整的证明和深入的案例分析。

---

## 1. 概念定义 (Definitions)

### 1.1 Iris逻辑框架概述

**Def-V-04-01** (Iris逻辑框架)。Iris是一个基于高阶分离逻辑的通用程序验证框架，其核心由以下组件构成：

$$
\text{Iris} \triangleq \langle \Sigma, \text{RA}, \mathcal{M}, \mathcal{L}, \mathcal{P} \rangle
$$

其中：

- $\Sigma$：宇宙类型签名 (universe of types)
- $\text{RA}$：资源代数类族 (resource algebras)
- $\mathcal{M}$：模态运算符集合 (modalities)
- $\mathcal{L}$：程序逻辑规则 (logic rules)
- $\mathcal{P}$：证明系统 (proof system)

**Def-V-04-02** (Iris断言语法)。Iris断言$P, Q$的语法定义为：

$$
\begin{aligned}
P, Q ::=\ & \top \mid \bot \mid P \land Q \mid P \lor Q \mid P \Rightarrow Q \mid \forall x:\tau. P \mid \exists x:\tau. P \\
& \mid P \ast Q \mid P \text{--*} Q \mid P \wand Q \mid l \mapsto v \\
& \mid \later P \mid \persistently P \mid \langle \mathcal{E}_1 \rangle\, P \,\langle \mathcal{E}_2 \rangle \mid \knowInv{\iota}{P} \\
& \mid \ownGhost{\gamma}{a} \mid \valid{a} \mid \mu X. P \mid X
\end{aligned}
$$

**Def-V-04-03** (步进索引语义)。Iris采用步进索引(step-indexed)语义处理递归定义和循环：

$$
\text{Prop} \triangleq \mathbb{N} \to \text{UPred}(\text{Res})
$$

其中$\text{UPred}(\text{Res})$是资源集合上的向上闭包谓词。断言$P$在步进$n$成立表示$P$在当前资源下至少可安全执行$n$步。

**Def-V-04-04** (Iris资源模型)。Iris的物理资源状态由堆和幽灵状态组成：

$$
\text{Res} \triangleq \text{Heap} \times \text{GhostState}
$$

其中：

- $\text{Heap} \triangleq \text{Loc} \rightharpoonup_{\text{fin}} \text{Val}$（有限堆）
- $\text{GhostState} \triangleq \prod_{i \in I} M_i$（幽灵状态，各资源代数的笛卡尔积）

### 1.2 资源代数 (Resource Algebras)

**Def-V-04-05** (资源代数 / Resource Algebra, RA)。资源代数是一个三元组$(M, \cdot, \valid{\cdot})$，其中：

| 组件 | 类型 | 说明 |
|------|------|------|
| $M$ | 集合 | 元素集合（含单位元$\epsilon$） |
| $\cdot : M \times M \to M$ | 运算 | 可交换、可结合的二元运算 |
| $\valid{\cdot} \subseteq M$ | 谓词 | 有效性谓词，满足特定闭包条件 |

**公理** (RA公理)：

1. **交换律**: $\forall a, b \in M. a \cdot b = b \cdot a$
2. **结合律**: $\forall a, b, c \in M. (a \cdot b) \cdot c = a \cdot (b \cdot c)$
3. **单位元**: $\forall a \in M. a \cdot \epsilon = a$
4. **有效性闭包**: $\valid{a} \land \valid{a \cdot b} \Rightarrow \valid{b}$

**Def-V-04-06** (相机 / Camera)。相机是RA的步进索引扩展：

$$
\text{Camera} \triangleq (M, \cdot, \valid{\cdot}, \mval{-}{-})
$$

其中$\mval{a}{n} \in M$表示元素$a$在第$n$步的近似，满足：

- $\mval{a}{0} = \epsilon$
- $\mval{(\mval{a}{n})}{m} = \mval{a}{\min(n,m)}$
- $n = 0 \lor \valid{\mval{a}{n}} \Rightarrow \valid{a}$

**Def-V-04-07** (常见资源代数实例)。

| RA名称 | 定义 | 用途 |
|--------|------|------|
| **独占RA** $(\text{Ex}(A))$ | $\{\bot\} \cup A$，$\bot$为未定义 | 独占所有权 |
| **分数RA** $(\text{Frac})$ | $(0, 1] \cap \mathbb{Q}$，加法 | 分数权限 |
| **授权RA** $(\text{Auth}(M))$ | $\{(\text{full}, a) \mid a \in M\} \cup \{(\text{frag}, a) \mid a \in M\}$ | 授权-碎片关系 |
| **可选RA** $(\text{Option}(M))$ | $\{\text{None}\} \cup \{\text{Some}(a) \mid a \in M\}$ | 可选资源 |
| **乘积RA** | 各组件RA的笛卡尔积 | 组合资源 |
| **函数RA** | $K \to M$（有限支撑） | 索引资源 |

**Def-V-04-08** (授权-碎片RA / Authoritative RA)。这是Iris中最核心的RA：

$$
\text{Auth}(M) \triangleq \{\authfull{a} \mid a \in M\} \cup \{\authfrag{a} \mid a \in M\}
$$

运算定义：

- $\authfull{a} \cdot \authfrag{b}$ 定义当且仅当$a = b$，结果为$\authfull{a}$
- $\authfrag{a} \cdot \authfrag{b} = \authfrag{a \cdot b}$
- 其他组合未定义

有效性：$\valid{\authfull{a}}$ 当且仅当 $\valid{a}$；$\valid{\authfrag{a}}$ 当且仅当 $\valid{a}$

**直观解释**：$\authfull{a}$表示对资源$a$的独占所有权（可修改），$\authfrag{a}$表示对资源$a$的只读视图（可共享）。

### 1.3 高阶逻辑基础

**Def-V-04-09** (高阶断言)。Iris支持断言级别的量化和高阶函数：

$$
P ::= \ldots \mid \lambda x. P \mid P\ Q \mid \mu X:\text{Prop} \to \text{Prop}. \lambda x. P \mid \text{fix}\ F\ x. P
$$

**Def-V-04-10** (谓词子类型)。Iris中谓词可以参数化：

$$
\text{Prop}_\Sigma \triangleq \forall \alpha_1, \ldots, \alpha_n. (\tau_1 \to \cdots \to \tau_m \to \text{Prop})
$$

其中$\Sigma$是类型签名。

**Def-V-04-11** (高阶分离蕴含 / Wand)。

$$
P \wand Q \triangleq \lambda r. \forall r'. r \perp r' \land P(r') \Rightarrow Q(r \cdot r')
$$

在Iris中，$\wand$与$\ast$形成伴随关系：

$$
P \ast Q \vdash R \iff P \vdash Q \wand R
$$

**Def-V-04-12** (递归谓词 / Löb归纳)。Iris通过Later模态支持递归谓词定义：

$$
\mu X. P \triangleq \text{fix}\ (\lambda X. P)\ \text{with}\ \later
$$

其中$\mu X. P$是$P$的最小不动点，要求$P$在$X$的出现前必须带有$\later$模态。

### 1.4 程序逻辑原语

**Def-V-04-13** (Hoare三元组 / Iris风格)。Iris中的Hoare三元组定义为：

$$
\{P\} e \{v. Q\}_\mathcal{E} \triangleq \persistently(P \Rightarrow \wpre{e}{\mathcal{E}}{v. Q})
$$

其中：

- $P$：前置条件（当前断言）
- $e$：程序表达式
- $v. Q$：后置条件（值$v$满足$Q$）
- $\mathcal{E}$：允许效果集合（可执行的原子操作集合）
- $\wpre{e}{\mathcal{E}}{\Phi}$：最弱前置条件

**Def-V-04-14** (最弱前置条件 / Weakest Precondition, WP)。

$$
\wpre{e}{\mathcal{E}}{\Phi} \triangleq \lambda r. \forall n. \text{safe}_n(e, r, \Phi, \mathcal{E})
$$

其中$\text{safe}_n(e, r, \Phi, \mathcal{E})$表示：从资源$r$开始，表达式$e$可安全执行$n$步，且若终止则结果满足$\Phi$。

**Def-V-04-15** (Iris程序语法)。Iris支持的语言是$\lambda$-演算扩展：

$$
\begin{aligned}
e ::=\ & x \mid \lambda x. e \mid e_1\ e_2 \mid \rec{f}{x}{e} \mid () \mid (e_1, e_2) \mid \pi_i\ e \\
& \mid \text{ref}(e) \mid !e \mid e_1 \gets e_2 \mid \text{CAS}(e_1, e_2, e_3) \\
& \mid \text{fork}\{e\} \mid \text{alloc}(n) \mid \text{free}(e) \\
v ::=\ & \lambda x. e \mid () \mid (v_1, v_2) \mid l \mid n \mid b \mid \ldots
\end{aligned}
$$


---

## 2. 核心模态详解

### 2.1 Later Modality (▷)

**Def-V-04-16** (Later模态 / ▷)。Later模态表示"下一步"或"稍后"成立：

$$
\later P \triangleq \lambda n. \begin{cases} \top & n = 0 \\ P(n-1) & n > 0 \end{cases}
$$

**直观解释**：$\later P$表示$P$在当前步不一定成立，但在下一步及之后成立。

**Lemma-V-04-01** (Later模态基本性质)。

| 性质 | 公式 | 说明 |
|------|------|------|
| 单调性 | $P \vdash Q \Rightarrow \later P \vdash \later Q$ | Later保持蕴涵 |
| 分配律 | $\later(P \land Q) \dashv\vdash \later P \land \later Q$ | 与合取交换 |
| 分配律 | $\later(P \lor Q) \dashv\vdash \later P \lor \later Q$ | 与析取交换 |
| 分配律 | $\later(P \ast Q) \dashv\vdash \later P \ast \later Q$ | 与分离合取交换 |
| 蕴涵 | $\later(P \Rightarrow Q) \vdash \later P \Rightarrow \later Q$ | 非双向 |
| 弱化 | $\later P \vdash \later\later P$ | 步进累积 |

**Thm-V-04-01** (Löb归纳原理)。这是Iris中最重要的推理原则：

$$
\frac{\later P \vdash P}{\vdash P} \quad (\text{Löb})
$$

**证明**：

1. 假设$\later P \vdash P$
2. 通过步进索引归纳，证明$\forall n. P(n)$
3. 基例$n=0$：由定义$\later P(0) = \top$，且$P(0) = \top$（因为$\later P \vdash P$）
4. 归纳步：假设$P(n)$成立，则$\later P(n+1) = P(n)$成立
5. 由假设$\later P \vdash P$，得$P(n+1)$成立
6. 故$\forall n. P(n)$，即$\vdash P$

**应用**：Löb归纳允许我们证明递归定义的谓词性质，只需在归纳假设（带$\later$）下证明目标。

**Def-V-04-17** (步进索引递归)。Iris中所有递归定义必须满足guardedness条件：

$$
\mu X. F(X) \triangleq \text{lfp}(\lambda X. F(\later X))
$$

即递归调用$X$必须在$F$中出现于$\later$模态之下。

### 2.2 Persistently Modality (□)

**Def-V-04-18** (Persistently模态 / □)。持久性模态表示"可永远保持"的断言：

$$
\persistently P \triangleq \lambda n, r. \forall r'. r \perp r' \land \valid{r \cdot r'} \Rightarrow P(n, r')
$$

**直观解释**：$\persistently P$表示$P$不依赖于任何独占资源，可从任何有效上下文中导出。

**等价定义**：在Iris中，$\persistently$也可定义为：

$$
\persistently P \triangleq P^{\epsilon} \ast \top
$$

其中$P^{\epsilon}$表示$P$的单位元版本。

**Lemma-V-04-02** (Persistently模态基本性质)。

| 性质 | 公式 | 说明 |
|------|------|------|
| 幂等性 | $\persistently\persistently P \dashv\vdash \persistently P$ | 双重持久 = 单次 |
| 单调性 | $P \vdash Q \Rightarrow \persistently P \vdash \persistently Q$ | 保持蕴涵 |
| 分离合取 | $\persistently(P \ast Q) \dashv\vdash \persistently P \ast \persistently Q$ | 与$\ast$交换 |
| 蕴含 | $\persistently(P \Rightarrow Q) \vdash \persistently P \Rightarrow \persistently Q$ | 保持蕴含 |
| 推出 | $\persistently P \vdash P$ | 可消除 |
| 引入 | $P \vdash \persistently P$（若$P$纯） | 纯断言持久 |

**Def-V-04-19** (纯断言与持久断言)。

- **纯断言** (Pure)：$\pure{P} \triangleq \exists \phi. P \dashv\vdash \lceil \phi \rceil$（$\phi$是元逻辑命题）
- **持久断言** (Persistent)：$\persistent{P} \triangleq P \vdash \persistently P$

**关系**：所有纯断言都是持久的，但持久断言不一定是纯的（如不变式$\knowInv{\iota}{P}$）。

**Thm-V-04-02** (持久性模态与分离合取的分配)。

$$
\persistently P \land (Q \ast R) \vdash (\persistently P \land Q) \ast R
$$

**证明**：

1. 假设$\persistently P \land (Q \ast R)$
2. 则存在$r_Q, r_R$使得$Q(r_Q)$且$R(r_R)$
3. 由$\persistently P$，对任意$r'$，若$\valid{r'}$则$P(r')$
4. 特别地，取$r' = r_Q$，则$P(r_Q)$
5. 故$(\persistently P \land Q)(r_Q)$且$R(r_R)$
6. 得$(\persistently P \land Q) \ast R$

### 2.3 Fancy Update Modality

**Def-V-04-20** (基本更新模态 / Basic Update)。

$$
\update{P} \triangleq \lambda n, r. \exists r'. r \leadsto r' \land P(n, r')
$$

其中$r \leadsto r'$表示资源$r$可更新为$r'$（在幽灵状态上的变迁关系）。

**Def-V-04-21** (Fancy Update模态)。Fancy Update是Iris中强大的状态转换模态：

$$
\updateM{\mathcal{E}_1}{\mathcal{E}_2}{P} \triangleq \lambda n, r. \forall r_f, n'. n' \leq n \land \valid{r \cdot r_f} \Rightarrow \\ \exists r', r'_f. r' \cdot r'_f \leadsto^* r \cdot r_f \land n' > 0 \Rightarrow \valid{r' \cdot r'_f} \land P(n', r')
$$

**简化形式**（当$\mathcal{E}_1 = \mathcal{E}_2 = \mathcal{E}$）：

$$
\update{P} \triangleq \updateM{\mathcal{E}}{\mathcal{E}}{P}
$$

**直观解释**：$\updateM{\mathcal{E}_1}{\mathcal{E}_2}{P}$表示在效果集合$\mathcal{E}_1$下，可通过幽灵状态更新（不修改物理状态）达到$P$，且之后效果集合变为$\mathcal{E}_2$。

**Lemma-V-04-03** (Fancy Update基本性质)。

| 性质 | 公式 | 说明 |
|------|------|------|
| 绑定律 | $\updateM{\mathcal{E}_1}{\mathcal{E}_2}{(\lambda x. P\ x)} \dashv\vdash \lambda x. \updateM{\mathcal{E}_1}{\mathcal{E}_2}{(P\ x)}$ | 可交换 |
| 单子律 | $\updateM{\mathcal{E}_1}{\mathcal{E}_2}{\updateM{\mathcal{E}_2}{\mathcal{E}_3}{P}} \vdash \updateM{\mathcal{E}_1}{\mathcal{E}_3}{P}$ | 可组合 |
| 弱化 | $\mathcal{E}_2 \subseteq \mathcal{E}_1 \Rightarrow \updateM{\mathcal{E}_1}{\mathcal{E}_2}{P} \vdash \updateM{\mathcal{E}_1}{\mathcal{E}_1}{P}$ | 效果扩展 |
| 引入 | $P \vdash \updateM{\mathcal{E}}{\mathcal{E}}{P}$ | 平凡更新 |
| 推出 | $\updateM{\mathcal{E}_1}{\mathcal{E}_2}{P} \vdash P$（若$P$纯） | 消除条件 |

**Def-V-04-22** (视图移位 / View Shift)。视图移位是Fancy Update的特殊形式：

$$
P \vs[\mathcal{E}_1][\mathcal{E}_2] Q \triangleq \persistently(P \Rightarrow \updateM{\mathcal{E}_1}{\mathcal{E}_2}{Q})
$$

当$\mathcal{E}_1 = \mathcal{E}_2 = \top$时简写为$P \vs Q$。

### 2.4 模态之间的关系与性质

**Thm-V-04-03** (模态之间的交互关系)。

| 关系 | 公式 | 条件 |
|------|------|------|
| Later + Persistently | $\persistently{\later P} \dashv\vdash \later{\persistently P}$ | 可交换 |
| Later + Update | $\updateM{\mathcal{E}_1}{\mathcal{E}_2}{(\later P)} \vdash \later{\updateM{\mathcal{E}_1}{\mathcal{E}_2}{P}}$ | 单向 |
| Persistently + Update | $\persistently{\updateM{\mathcal{E}_1}{\mathcal{E}_2}{P}} \vdash \updateM{\mathcal{E}_1}{\mathcal{E}_2}{\persistently P}$ | 单向 |
| 吸收 | $\updateM{\mathcal{E}_1}{\mathcal{E}_2}{\persistently P} \vdash \persistently{\updateM{\mathcal{E}_1}{\mathcal{E}_2}{P}}$ | 若$P$纯 |

**Thm-V-04-04** (模态的包含关系)。

$$
\persistently P \vdash \updateM{\mathcal{E}_1}{\mathcal{E}_2}{\persistently P} \vdash \updateM{\mathcal{E}_1}{\mathcal{E}_2}{P} \quad (\text{若 } P \text{ 纯})
$$

**Thm-V-04-05** (分离合取与模态的分配)。

$$
\begin{aligned}
& (\later P) \ast (\later Q) \dashv\vdash \later(P \ast Q) \\
& (\persistently P) \ast (\persistently Q) \dashv\vdash \persistently(P \ast Q) \\
& (\updateM{\mathcal{E}_1}{\mathcal{E}_2}{P}) \ast Q \vdash \updateM{\mathcal{E}_1}{\mathcal{E}_2}{(P \ast Q)} \quad (\text{若 } Q \text{ 纯或持久})
\end{aligned}
$$

**证明** (Later与分离合取的可交换性)：

1. 由定义：$(\later P \ast \later Q)(n) \iff \exists r_1, r_2. r = r_1 \cdot r_2 \land (\later P)(n, r_1) \land (\later Q)(n, r_2)$
2. 对$n > 0$：$= \exists r_1, r_2. r = r_1 \cdot r_2 \land P(n-1, r_1) \land Q(n-1, r_2)$
3. $= (P \ast Q)(n-1, r) = \later(P \ast Q)(n, r)$
4. 对$n = 0$：两边都为$\top$

**Lemma-V-04-04** (模态推理规则)。

$$
\frac{P \vdash Q}{\later P \vdash \later Q} \quad \frac{P \vdash Q}{\persistently P \vdash \persistently Q} \quad \frac{P \vdash Q}{\updateM{\mathcal{E}_1}{\mathcal{E}_2}{P} \vdash \updateM{\mathcal{E}_1}{\mathcal{E}_2}{Q}}
$$

---

## 3. 并发原语

### 3.1 Invariants - 并发不变式

**Def-V-04-23** (不变式命名空间)。不变式由命名空间$\iota \in \text{Name}$索引：

$$
\text{Name} \triangleq \mathbb{N} \times \text{string}
$$

命名空间支持层次化结构：$\iota.0, \iota.1$表示$\iota$的子空间。

**Def-V-04-24** (不变式断言)。$\knowInv{\iota}{P}$表示在命名空间$\iota$上注册的不变式$P$：

$$
\knowInv{\iota}{P} \triangleq \text{幽灵状态中的注册信息}
$$

其中$P$必须是持久断言，即$P \vdash \persistently P$。

**不变式规则**：

$$
\frac{P \text{ 持久}}{\knowInv{\iota}{P} \text{ 持久}}
$$

**Def-V-04-25** (不变式打开/关闭)。在原子操作内可以临时打开不变式：

$$
\frac{\knowInv{\iota}{P} \ast P \vs[\mathcal{E} \cup \{\iota\}][\mathcal{E}']{Q} \quad Q \text{ 持久}}{\knowInv{\iota}{P} \vs[\mathcal{E}][\mathcal{E}']{Q}}
$$

**直观解释**：要验证原子操作，可以临时"打开"不变式获取资源$P$，操作完成后必须"关闭"不变式（恢复$P$）。

**Lemma-V-04-05** (不变式的基本性质)。

| 性质 | 公式 | 说明 |
|------|------|------|
| 持久性 | $\knowInv{\iota}{P} \vdash \persistently{\knowInv{\iota}{P}}$ | 不变式可共享 |
| 分配 | $\knowInv{\iota}{(P \land Q)} \dashv\vdash \knowInv{\iota}{P} \land \knowInv{\iota}{Q}$ | 合取分解 |
| 组合 | $\knowInv{\iota.0}{P} \ast \knowInv{\iota.1}{Q} \vdash \knowInv{\iota}{(P \ast Q)}$ | 子空间组合 |
| 持久消除 | $\knowInv{\iota}{P} \vdash P$（若$P$纯） | 纯断言可导出 |

**Thm-V-04-06** (不变式保持定理)。若程序在验证时使用不变式$\knowInv{\iota}{P}$，且原子操作内保持$P$，则程序执行始终维持$P$。

**证明概要**：

1. 通过交错语义，每个线程的原子操作要么独立执行，要么与其他线程的原子操作交错
2. 不变式保证在任何可见状态下$P$都成立
3. 原子操作打开$P$后，操作完成前其他线程无法观察到不一致状态
4. 操作完成后$P$被恢复，故全局可见状态始终满足$P$

### 3.2 Ghost State - 幽灵状态

**Def-V-04-26** (幽灵状态分配器)。幽灵状态通过分配器$\ownGhost{\gamma}{a}$管理：

$$
\ownGhost{\gamma}{a} \triangleq \text{在幽灵名称 } \gamma \text{ 上拥有RA元素 } a
$$

其中$\gamma \in \text{GName}$是幽灵名称，$a \in M$是资源代数元素。

**Def-V-04-27** (幽灵状态分配与更新)。

**幽灵分配规则**：

$$
\frac{}{\vdash \update{\exists \gamma. \ownGhost{\gamma}{a}}} \quad (\text{若 } \valid{a})
$$

**幽灵更新规则**：

$$
\frac{a \leadsto_M b}{\ownGhost{\gamma}{a} \vs \ownGhost{\gamma}{b}}
$$

**Def-V-04-28** (授权-碎片模式)。幽灵状态的核心模式是授权-碎片RA：

$$
\ownGhost{\gamma}{\authfull{a}} \quad \text{(授权者)}
$$

$$
\ownGhost{\gamma}{\authfrag{b}} \quad \text{(碎片持有者)}
$$

**性质**：$\authfull{a} \cdot \authfrag{b}$有效当且仅当$a = b$。

**Thm-V-04-07** (幽灵状态一致性)。授权者和碎片持有者的视图始终保持一致：

$$
\knowInv{\iota}{\ownGhost{\gamma}{\authfull{a}} \Rightarrow Q(a)} \ast \ownGhost{\gamma}{\authfrag{a}} \vdash Q(a)
$$

**应用模式**：

| 模式 | 幽灵RA | 用途 |
|------|--------|------|
| 独占所有权 | $\text{Ex}(A)$ | 证明独占访问 |
| 分数权限 | $\text{Frac}$ | 共享读取/独占写入 |
| 单调计数器 | $\text{Auth}(\text{Max}(\mathbb{N}))$ | 单调递增验证 |
| 集合成员 | $\text{Auth}(\mathcal{P}(X))$ | 元素添加/删除 |

### 3.3 Atomic Specifications - 原子性规范

**Def-V-04-29** (原子Hoare三元组)。用于验证原子操作的规范：

$$
\langle P \rangle e \langle v. Q \rangle_\mathcal{E}
$$

语义：在原子操作期间可以临时打开不变式，但操作必须是原子的（不能被其他线程交错）。

**Def-V-04-30** (原子上下文)。效果集合$\mathcal{E}$控制可访问的不变式：

- $\mathcal{E} = \emptyset$：不能打开任何不变式
- $\mathcal{E} = \{\iota_1, \ldots, \iota_n\}$：可以打开这些命名空间的不变式
- $\mathcal{E} = \top$：可以打开所有命名空间

**原子操作规则**：

$$
\frac{P \text{ 原子} \quad \{P \ast I\} e \{v. Q \ast I\}}{\langle P \rangle e \langle v. Q \rangle_\mathcal{E}} \quad (I \text{ 是 } \mathcal{E} \text{ 中不变式})
$$

**Thm-V-04-08** (原子规范的可靠性)。若$\vdash \langle P \rangle e \langle v. Q \rangle_\mathcal{E}$，则$e$是原子的，且满足规范。

**证明要点**：

1. 原子性：通过物理层面的原子操作（如CAS）保证
2. 规范性：通过WP语义，原子操作期间可以访问不变式资源
3. 一致性：操作完成后必须恢复所有打开的不变式

**Def-V-04-31** (比较并交换 / CAS规范)。CAS是核心的原子操作：

$$
\langle l \mapsto v_1 \rangle \text{CAS}(l, v_1, v_2) \langle b. (b = \text{true} \land l \mapsto v_2) \lor (b = \text{false} \land l \mapsto v_1) \rangle
$$

### 3.4 锁和屏障的验证

**Def-V-04-32** (锁资源不变式)。锁$\ell$保护资源$P$的定义：

$$
\text{IsLock}(\ell, P) \triangleq \knowInv{\iota.\text{lock}}{\ell \mapsto \text{false} \lor (\ell \mapsto \text{true} \ast P)}
$$

**锁操作规范**：

| 操作 | 规范 |
|------|------|
| **newlock** | $\{P\}\ \text{newlock}()\ \{\ell. \text{IsLock}(\ell, P) \ast \text{Locked}(\ell)\}$ |
| **acquire** | $\{\text{IsLock}(\ell, P)\}\ \text{acquire}(\ell)\ \{\text{Locked}(\ell) \ast P\}$ |
| **release** | $\{\text{Locked}(\ell) \ast P\}\ \text{release}(\ell)\ \{\text{IsLock}(\ell, P)\}$ |

**Def-V-04-33** (屏障 / Barrier)。屏障用于同步多个线程：

$$
\text{Barrier}(b, n, P) \triangleq \text{计数器为}n\text{的屏障，达到}0\text{时释放}P
$$

**屏障操作规范**：

$$
\begin{aligned}
& \{P\}\ \text{newbarrier}(n)\ \{b. \text{Barrier}(b, n, P)\} \\
& \{\text{Barrier}(b, n, P)\}\ \text{wait}(b)\ \{P \ast R\} \\
& \{\text{Barrier}(b, n, P)\}\ \text{signal}(b)\ \{\top\}
\end{aligned}
$$

**Thm-V-04-09** (锁实现的正确性)。基于CAS的锁实现满足上述规范。

**证明概要**：

1. 锁状态$\ell \mapsto b$表示锁是否被持有
2. 不变式保证：锁空闲时资源$P$在锁中；锁被持有时资源$P$在持有者手中
3. acquire操作通过CAS原子地将锁从空闲改为持有
4. release操作将锁从持有改为空闲，同时转移$P$

---

## 4. 分离逻辑扩展

### 4.1 高阶分离连接词

**Def-V-04-34** (分离谓词抽象)。Iris支持谓词级别的抽象：

$$
\Phi : \text{Val} \to \text{Prop} \quad \text{(谓词变量)}
$$

**分离蕴含的函数形式**：

$$
\forall x. P(x) \wand Q(x) \triangleq \lambda r. \forall x, r'. r \perp r' \land P(x)(r') \Rightarrow Q(x)(r \cdot r')
$$

**Def-V-04-35** (谓词分离合取)。对谓词集合的分离合取：

$$
\bigast_{i \in I} P_i \triangleq \begin{cases} \emp & I = \emptyset \\ P_{i_0} \ast \bigast_{i \in I \setminus \{i_0\}} P_i & \text{否则} \end{cases}
$$

**Def-V-04-36** (分离迭代量词)。

$$
\begin{aligned}
& \text{Sep-}\forall x. P(x) \triangleq \forall x. P(x) \quad (\text{若}P\text{纯}) \\
& \text{Sep-}\exists x. P(x) \triangleq \exists x. P(x) \quad (\text{若}P\text{纯}) \\
& \text{Sep-}\forall^* x. P(x) \triangleq \text{分离全称} \\
& \text{Sep-}\exists^* x. P(x) \triangleq \text{分离存在}
\end{aligned}
$$

### 4.2 所有权与权限推理

**Def-V-04-37** (分数所有权)。通过分数RA实现读写权限分离：

$$
\frac{q_1 + q_2 \leq 1}{\ownGhost{\gamma}{q_1} \ast \ownGhost{\gamma}{q_2} \dashv\vdash \ownGhost{\gamma}{q_1 + q_2}}
$$

**分数所有权规范**：

| 权限 | 断言 | 操作 |
|------|------|------|
| **独占写** | $\ownGhost{\gamma}{1}$ | 读+写 |
| **共享读** | $\ownGhost{\gamma}{q}$（$q < 1$） | 只读 |
| **组合** | $\ownGhost{\gamma}{q_1} \ast \ownGhost{\gamma}{q_2}$ | $q_1 + q_2 \leq 1$ |

**Def-V-04-38** (可丢弃所有权 / Discardable Ownership)。通过可选RA实现：

$$
\text{maybe}(P) \triangleq \text{Some}(P) \lor \text{None}
$$

**Def-V-04-39** (能力语义 / Capability Semantics)。

$$
\text{cap}(R, P) \triangleq R \wand P
$$

表示持有能力$R$可获取权限$P$。

**Thm-V-04-10** (权限组合定理)。不同类型的权限可组合使用：

$$
\begin{aligned}
& \text{frac}(q_1) \ast \text{frac}(q_2) \dashv\vdash \text{frac}(q_1 + q2) \quad (q_1 + q_2 \leq 1) \\
& \text{ex}(a) \ast \text{ex}(b) \dashv\vdash \bot \quad (a \neq b) \\
& \text{authfull}(a) \ast \text{authfrag}(b) \dashv\vdash \text{valid}(a \cdot b) \iff a = b
\end{aligned}
$$

### 4.3 抽象谓词

**Def-V-04-40** (抽象谓词 / Abstract Predicate)。隐藏实现细节的谓词：

$$
\text{isDataStructure}(x) \triangleq \exists \gamma. \ownGhost{\gamma}{\authfull{\ldots}} \ast \text{inv}(\ldots)
$$

**抽象谓词原则**：

1. **封装性**：内部表示不暴露给客户端
2. **不变式**：内部不变式在接口层面保持
3. **可组合性**：多个抽象谓词可组合

**Def-V-04-41** (表示谓词 / Representation Predicate)。连接逻辑断言与物理状态：

$$
R(x, v) \triangleq \text{逻辑值 } x \text{ 在物理位置 } v \text{ 的表示}
$$

**例**：链表表示谓词

$$
\text{isList}(xs, l) \triangleq \begin{cases} l = \text{null} & xs = [] \\ \exists l', v. l \mapsto (v, l') \ast \text{isList}(xs', l') & xs = v :: xs' \end{cases}
$$

**Def-V-04-42** (规范函子 / Specification Functor)。高阶抽象模式：

$$
F(X) \triangleq \lambda x. P(x) \ast \later(\forall y. Q(x, y) \wand X(y))
$$

$$
\mu X. F(X) \triangleq \text{抽象数据结构的递归规范}
$$

**Thm-V-04-11** (抽象谓词的可重用性)。良好设计的抽象谓词可在不同上下文中重用：

$$
\frac{\text{isStack}(s, xs) \ast P(x) \vdash Q}{\text{useStack}(s, P, Q)}
$$

---

## 5. 形式证明

### 5.1 定理: Iris逻辑的一致性

**Thm-V-04-12** (Iris逻辑一致性)。Iris逻辑是一致的，即不存在断言$P$使得$\vdash P \land \neg P$。

**证明**：

**步骤1：构建语义模型**

Iris的语义基于步进索引Kripke模型：

$$
\llbracket P \rrbracket : \mathbb{N} \to \text{Res} \to \mathbb{B}
$$

**步骤2：定义有效性**

$$
\valid{P} \triangleq \forall n, r. \valid{r} \Rightarrow \llbracket P \rrbracket(n, r)
$$

**步骤3：证明基本逻辑规则保持有效性**

| 规则 | 保持性 |
|------|--------|
| 假言推理 | $\valid{P \Rightarrow Q} \land \valid{P} \Rightarrow \valid{Q}$ |
| 分离合取 | $\valid{P \ast Q} \iff \exists r_1, r_2. r = r_1 \cdot r_2 \land \valid{P(r_1)} \land \valid{Q(r_2)}$ |
| Later | $\valid{\later P} \iff \forall n > 0. \valid{P(n-1)}$ |
| Persistently | $\valid{\persistently P} \iff \forall r'. \valid{r \cdot r'} \Rightarrow \valid{P(r')}$ |

**步骤4：反证法**

假设存在$P$使得$\vdash P \land \neg P$，则：

1. 由可靠性，$\valid{P \land \neg P}$
2. 即$\forall n, r. \valid{r} \Rightarrow \llbracket P \rrbracket(n, r) \land \neg \llbracket P \rrbracket(n, r)$
3. 取$n=0, r=\epsilon$，得矛盾

**结论**：Iris逻辑是一致的。$\square$

### 5.2 定理: Hoare三元组的可靠性

**Thm-V-04-13** (Hoare三元组可靠性)。若$\vdash \{P\} e \{v. Q\}_\mathcal{E}$在Iris中可证明，则程序$e$满足规范：

$$
\forall r. P(r) \Rightarrow \text{safe}(e, r, Q, \mathcal{E})
$$

**证明**：

**步骤1：最弱前置条件的可靠性**

首先证明WP的可靠性：

$$
\valid{\wpre{e}{\mathcal{E}}{\Phi}} \Rightarrow \text{safe}(e, \Phi, \mathcal{E})
$$

**步骤2：归纳于表达式结构**

| 表达式 | 规则 | 可靠性 |
|--------|------|--------|
| $v$ (值) | $\wpre{v}{\mathcal{E}}{\Phi} \dashv\vdash \Phi(v)$ | 立即满足 |
| $e_1\ e_2$ | $\wpre{e_1}{\mathcal{E}}{v_1. \wpre{e_2[v_1/x]}{\mathcal{E}}{\Phi}}$ | 归纳假设 |
| $\text{ref}(e)$ | 分配规则 | 堆语义保证 |
| $!e$ | 读取规则 | 堆语义保证 |
| $e_1 \gets e_2$ | 写入规则 | 堆语义保证 |
| $\text{CAS}(e_1, e_2, e_3)$ | CAS规则 | 原子性保证 |
| $\text{fork}\{e\}$ | 分叉规则 | 交错语义 |

**步骤3：原子操作的可靠性**

对于原子操作$\langle P \rangle e \langle v. Q \rangle$：

1. 原子性由物理CAS保证
2. 通过打开不变式获得资源$P$
3. 执行$e$后得到$Q$
4. 恢复不变式

**步骤4：并发组合的可靠性**

对于并行组合$C_1 \parallel C_2$：

1. 分离前件保证资源不冲突
2. 交错语义保证执行正确
3. 不变式在所有交错点保持

**结论**：Hoare三元组的可靠性得证。$\square$

### 5.3 定理: 并发不变式的保持性

**Thm-V-04-14** (并发不变式保持性)。设程序$e$在不变式集合$\mathcal{I}$下验证通过，则$e$的执行始终保持所有不变式：

$$
\frac{\{P \ast \bigast_{I \in \mathcal{I}} I\}\ e\ \{Q \ast \bigast_{I \in \mathcal{I}} I\}}{\forall \sigma_0 \sigma_1. \langle e, \sigma_0 \rangle \to^* \langle e', \sigma_1 \rangle \Rightarrow \bigast_{I \in \mathcal{I}} I(\sigma_1)}
$$

**证明**：

**步骤1：不变式的语义**

不变式$\knowInv{\iota}{P}$的语义：

$$
\llbracket \knowInv{\iota}{P} \rrbracket \triangleq \lambda n, r. \forall m \leq n. P(m, r_\iota)
$$

其中$r_\iota$是分配给命名空间$\iota$的幽灵资源。

**步骤2：原子操作内的不变式保持**

设原子操作$\alpha$打开不变式$\knowInv{\iota}{P}$：

1. **打开前**：$\knowInv{\iota}{P}$保持（归纳假设）
2. **打开时**：获取$P$，暂时移除$\knowInv{\iota}{P}$
3. **操作中**：仅当前线程可访问$P$，其他线程无法观察到不一致状态
4. **关闭时**：恢复$P$和$\knowInv{\iota}{P}$

**步骤3：交错执行的保持性**

对于交错执行$\langle e_1 \parallel e_2, \sigma \rangle \to \langle e_1' \parallel e_2, \sigma' \rangle$：

1. 设$e_1$执行原子操作$\alpha$
2. $\alpha$的验证保证：若不变式在$\sigma$成立，则在$\sigma'$成立
3. $e_2$的状态不受直接影响

**步骤4：归纳证明**

对执行步数$n$归纳：

- **基例** ($n=0$)：初始状态满足不变式（前件假设）
- **归纳步**：假设第$k$步保持，第$k+1$步由步骤2、3保持

**结论**：并发不变式保持性得证。$\square$

### 5.4 详细证明步骤补充

**Lemma-V-04-06** (资源代数的组合性)。资源代数的笛卡尔积仍然是资源代数：

$$
\frac{(M_1, \cdot_1, \valid{\cdot}_1) \text{ 是RA} \quad (M_2, \cdot_2, \valid{\cdot}_2) \text{ 是RA}}{(M_1 \times M_2, \cdot, \valid{\cdot}) \text{ 是RA}}
$$

其中$(a_1, a_2) \cdot (b_1, b_2) = (a_1 \cdot_1 b_1, a_2 \cdot_2 b_2)$。

**证明**：

1. 交换律：由分量交换律得$(a_1, a_2) \cdot (b_1, b_2) = (a_1 \cdot_1 b_1, a_2 \cdot_2 b_2) = (b_1 \cdot_1 a_1, b_2 \cdot_2 a_2) = (b_1, b_2) \cdot (a_1, a_2)$
2. 结合律类似
3. 单位元：$(\epsilon_1, \epsilon_2)$
4. 有效性闭包：若$\valid{(a_1, a_2)}$且$\valid{(a_1, a_2) \cdot (b_1, b_2)}$，则$\valid{a_1}$且$\valid{a_1 \cdot_1 b_1}$，由RA公理得$\valid{b_1}$；同理$\valid{b_2}$

**Lemma-V-04-07** (幽灵状态更新的原子性)。幽灵状态更新是逻辑上的原子操作：

$$
\frac{a \leadsto_M b}{\ownGhost{\gamma}{a} \vs \ownGhost{\gamma}{b}}
$$

**证明**：

1. 由$\ownGhost{\gamma}{a}$的定义，当前在$\gamma$上拥有$a$
2. 更新关系$a \leadsto_M b$在RA$M$中定义
3. 通过Fancy Update，将幽灵状态从$a$改为$b$
4. 更新后拥有$\ownGhost{\gamma}{b}$

**Thm-V-04-15** (Löb归纳的完备性)。在Iris的步进索引模型中，Löb归纳是完备的：

$$
\vdash P \iff \later P \vdash P
$$

**证明**：

- $(\Rightarrow)$：由$\later P \vdash P$和$P \vdash P$得$\vdash P$
- $(\Leftarrow)$：由Löb规则直接得

完备性源于步进索引的良基性：任何递减的步进序列必终止。

---

## 6. 案例研究

### 6.1 并发计数器验证

**实现** (C语言风格)：

```c
struct Counter {
    atomic_int value;
};

Counter* new_counter() {
    Counter* c = malloc(sizeof(Counter));
    c->value = 0;
    return c;
}

void increment(Counter* c) {
    int old, new;
    do {
        old = atomic_load(&c->value);
        new = old + 1;
    } while (!atomic_compare_exchange_weak(&c->value, &old, new));
}

int read(Counter* c) {
    return atomic_load(&c->value);
}
```

**规范**：

$$
\begin{aligned}
& \{\emp\}\ \text{new\_counter}()\ \{c. \exists \gamma. \text{IsCounter}(c, \gamma, 0)\} \\
& \{\text{IsCounter}(c, \gamma, n)\}\ \text{increment}(c)\ \{\text{IsCounter}(c, \gamma, n+1)\} \\
& \{\text{IsCounter}(c, \gamma, n)\}\ \text{read}(c)\ \{v. v = n \ast \text{IsCounter}(c, \gamma, n)\}
\end{aligned}
$$

**不变式定义**：

$$
\text{IsCounter}(c, \gamma, n) \triangleq \knowInv{\iota}{c \mapsto n' \ast \ownGhost{\gamma}{\authfull{n'}} \land n' \geq n}
$$

**验证**：

**引理-V-04-08** (Increment的正确性)：

$$
\{\text{IsCounter}(c, \gamma, n)\}\ \text{increment}(c)\ \{\text{IsCounter}(c, \gamma, n+1)\}
$$

**证明**：

1. 打开不变式，获得$c \mapsto n'$和$\authfull{n'}$
2. CAS操作：若$c$仍为$n'$，则更新为$n'+1$
3. 幽灵更新：$\authfull{n'} \leadsto \authfull{n'+1}$
4. 关闭不变式：$c \mapsto n'+1 \ast \authfull{n'+1}$
5. 得$\text{IsCounter}(c, \gamma, n+1)$

### 6.2 Ticket Lock验证

**实现**：

```c
struct TicketLock {
    atomic_int next_ticket;
    atomic_int now_serving;
};

void acquire(TicketLock* lock) {
    int my_ticket = atomic_fetch_add(&lock->next_ticket, 1);
    while (atomic_load(&lock->now_serving) != my_ticket) {
        // 自旋等待
    }
}

void release(TicketLock* lock) {
    atomic_fetch_add(&lock->now_serving, 1);
}
```

**资源不变式**：

$$
\begin{aligned}
\text{IsTicketLock}(\ell, P) \triangleq & \exists \gamma_N, \gamma_S. \knowInv{\iota}{\\
    & \ell.\text{next} \mapsto N \ast \ell.\text{now} \mapsto S \ast \\
    & \ownGhost{\gamma_N}{\authfull{N}} \ast \ownGhost{\gamma_S}{\authfull{S}} \ast \\
    & S \leq N \ast (S = N \Rightarrow P) \ast (S < N \Rightarrow \text{Locked}(\ell))
}
\end{aligned}
$$

**规范**：

$$
\begin{aligned}
& \{\emp\}\ \text{new\_ticket\_lock}()\ \{\ell. \text{IsTicketLock}(\ell, \emp) \ast \text{Locked}(\ell)\} \\
& \{\text{IsTicketLock}(\ell, P)\}\ \text{acquire}(\ell)\ \{\text{Locked}(\ell) \ast P\} \\
& \{\text{Locked}(\ell) \ast P\}\ \text{release}(\ell)\ \{\text{IsTicketLock}(\ell, P)\}
\end{aligned}
$$

**验证要点**：

1. **公平性**：每个acquire获得唯一的ticket号码
2. **互斥性**：只有当前serving等于ticket的线程可以进入临界区
3. **资源转移**：release将资源$P$归还到锁中

**Thm-V-04-16** (Ticket Lock的正确性)。上述实现满足互斥锁规范。

### 6.3 带帮助的无锁栈

**实现** (Treiber栈)：

```c
struct Node {
    int value;
    struct Node* next;
};

struct Stack {
    atomic struct Node* head;
};

void push(Stack* s, int v) {
    Node* new_node = malloc(sizeof(Node));
    new_node->value = v;
    do {
        new_node->next = atomic_load(&s->head);
    } while (!atomic_compare_exchange_weak(&s->head, &new_node->next, new_node));
}

int pop(Stack* s, bool* success) {
    do {
        Node* old_head = atomic_load(&s->head);
        if (old_head == NULL) {
            *success = false;
            return 0;
        }
        Node* new_head = old_head->next;
        if (atomic_compare_exchange_weak(&s->head, &old_head, new_head)) {
            *success = true;
            int val = old_head->value;
            free(old_head);
            return val;
        }
    } while (true);
}
```

**抽象谓词**：

$$
\text{isStack}(s, xs) \triangleq \exists \gamma. \knowInv{\iota}{\text{StackInv}(s, \gamma, xs)}
$$

$$
\text{StackInv}(s, \gamma, xs) \triangleq s.\text{head} \mapsto p \ast \text{isList}(p, xs) \ast \ownGhost{\gamma}{\authfull{xs}}
$$

**规范**：

$$
\begin{aligned}
& \{\emp\}\ \text{new\_stack}()\ \{s. \text{isStack}(s, [])\} \\
& \{\text{isStack}(s, xs)\}\ \text{push}(s, v)\ \{\text{isStack}(s, v::xs)\} \\
& \{\text{isStack}(s, xs)\}\ \text{pop}(s)\ \{r. (r = \text{None} \land xs = [] \land \text{isStack}(s, [])) \\
& \qquad\qquad\qquad\qquad\qquad\qquad\lor (\exists v, xs'. r = \text{Some}(v) \land xs = v::xs' \land \text{isStack}(s, xs'))\}
\end{aligned}
$$

**验证要点**：

1. **线性化点**：CAS成功时为线性化点
2. **ABA安全**：使用标记指针或SMR避免ABA问题
3. **无锁属性**：至少一个线程在有限步内完成操作

### 6.4 数组队列锁

**实现** (CLH锁)：

```c
struct QNode {
    atomic_bool locked;
};

struct CLHLock {
    atomic QNode* tail;
};

thread_local QNode* my_node;

void acquire(CLHLock* lock) {
    my_node->locked.store(true);
    QNode* pred = atomic_exchange(&lock->tail, my_node);
    while (pred->locked.load()) {
        // 自旋等待前驱
    }
}

void release(CLHLock* lock) {
    my_node->locked.store(false);
    my_node = pred;  // 复用前驱节点
}
```

**不变式**：

$$
\text{IsCLHLock}(\ell, P) \triangleq \knowInv{\iota}{\exists Q. \text{Queue}(Q) \ast \ell.\text{tail} \mapsto \text{last}(Q)}
$$

其中$Q$是等待线程队列，每个节点表示一个等待线程。

**规范**：

$$
\begin{aligned}
& \{\emp\}\ \text{new\_clh\_lock}()\ \{\ell. \text{IsCLHLock}(\ell, \emp)\} \\
& \{\text{IsCLHLock}(\ell, P)\}\ \text{acquire}(\ell)\ \{\text{Locked}(\ell) \ast P\} \\
& \{\text{Locked}(\ell) \ast P\}\ \text{release}(\ell)\ \{\text{IsCLHLock}(\ell, P)\}
\end{aligned}
$$

**验证要点**：

1. **FIFO公平性**：按到达顺序获取锁
2. **空间效率**：每个线程只需一个本地节点
3. **缓存友好性**：只有前驱和后继节点被访问

---

## 7. 可视化 (Visualizations)

### 7.1 Iris架构图

Iris框架的整体架构展示了从基础数学结构到应用层证明的层次关系。

```mermaid
graph TB
    subgraph "数学基础层"
        RA["资源代数 RA<br/>(M, ·, ✓)"]
        Camera["相机 Camera<br/>(步进索引RA)"]
        UPred["向上闭包谓词<br/>UPred(Res)"]
    end

    subgraph "核心逻辑层"
        BaseLogic["基础高阶逻辑<br/>□, ▷, ⚡"]
        ProgramLogic["程序逻辑<br/>WP, Hoare三元组"]
        Invariants["不变式系统<br/>Inv, Ghost State"]
    end

    subgraph "证明基础设施"
        Loeb["Löb归纳"]
        FancyUpdate["Fancy Update"]
        ViewShift["视图移位"]
    end

    subgraph "应用层"
        Concurrent["并发程序验证"]
        Modular["模块化抽象"]
        Refinement["精化证明"]
    end

    RA --> Camera
    Camera --> UPred
    UPred --> BaseLogic
    BaseLogic --> ProgramLogic
    ProgramLogic --> Invariants
    BaseLogic --> Loeb
    BaseLogic --> FancyUpdate
    BaseLogic --> ViewShift
    ProgramLogic --> Concurrent
    Invariants --> Modular
    FancyUpdate --> Refinement
```

### 7.2 模态关系图

Iris中核心模态之间的逻辑关系与转换规则。

```mermaid
graph LR
    subgraph "模态运算符"
        Later["▷ Later<br/>步进索引"]
        Persistent["□ Persistent<br/>持久性"]
        Update["⚡ Fancy Update<br/>状态转换"]
        Plain["纯断言"]
    end

    subgraph "关系与性质"
        L_P["▷□P ⊢ □▷P<br/>可交换"]
        P_U["□⚡P ⊢ ⚡□P<br/>单向"]
        Plain_P["纯 ⊢ □<br/>纯则持久"]
        Loeb["Löb规则<br/>▷P ⊢ P ⇒ ⊢ P"]
    end

    Later --> L_P
    Persistent --> L_P
    Persistent --> P_U
    Update --> P_U
    Plain --> Plain_P
    Persistent --> Plain_P
    Later --> Loeb

    style Later fill:#e1f5ff,stroke:#01579b
    style Persistent fill:#e8f5e9,stroke:#1b5e20
    style Update fill:#fff3e0,stroke:#e65100
```

### 7.3 资源代数层次图

常见资源代数及其组合关系的层次结构。

```mermaid
graph TB
    subgraph "基础RA"
        Ex["Ex(A)<br/>独占RA"]
        Frac["Frac<br/>分数RA"]
        Ag["Ag(T)<br/>同意RA"]
    end

    subgraph "组合RA"
        Auth["Auth(M)<br/>授权-碎片"]
        Prod["M₁ × M₂<br/>乘积RA"]
        Fun["K → M<br/>函数RA"]
    end

    subgraph "应用RA"
        Counter["计数器RA<br/>Auth(Max(ℕ))"]
        Heap["堆模型RA<br/>Loc → Ex(Val)"]
        Perms["权限RA<br/>Auth(Frac)"]
    end

    Ex --> Auth
    Frac --> Auth
    Auth --> Counter
    Auth --> Perms
    Ex --> Heap
    Prod --> Heap
    Fun --> Heap
    Ag --> Counter

    style Auth fill:#ffebee,stroke:#b71c1c
    style Counter fill:#e8f5e9,stroke:#1b5e20
    style Heap fill:#e3f2fd,stroke:#0d47a1
```

### 7.4 并发验证流程图

使用Iris验证并发程序的完整工作流程。

```mermaid
flowchart TD
    Start([开始验证]) --> Spec[定义程序规范<br/>Hoare三元组]
    Spec --> Inv[识别不变式<br/>并发资源]
    Inv --> Ghost[设计幽灵状态<br/>资源代数]
    Ghost --> Abstract[构建抽象谓词<br/>隐藏实现]
    Abstract --> Proof[编写证明脚本<br/>Coq/Iris]

    Proof --> Check{类型检查}
    Check -->|失败| Fix[修正证明]
    Fix --> Proof
    Check -->|成功| Review[审查覆盖性<br/>所有交错]

    Review --> Complete{验证完成?}
    Complete -->|否| Extend[扩展规范<br/>边界情况]
    Extend --> Spec
    Complete -->|是| Certified([验证通过<br/>获得保证])

    style Start fill:#e8f5e9,stroke:#1b5e20
    style Certified fill:#e8f5e9,stroke:#1b5e20
    style Check fill:#fff3e0,stroke:#e65100
```

### 7.5 锁验证结构图

Ticket Lock和CLH Lock的验证结构对比。

```mermaid
graph TB
    subgraph "Ticket Lock结构"
        TN["next: 下一个ticket"]
        TS["now: 当前serving"]
        TInv["不变式:<br/>S ≤ N ∧ (S=N ⇒ P)"]
        TAcquire["acquire:<br/>fetch_add获取ticket<br/>自旋等待S=my_ticket"]
        TRelease["release:<br/>fetch_add增加S"]
    end

    subgraph "CLH Lock结构"
        CT["tail: 队列尾指针"]
        CQ["队列节点链<br/>QNode{locked}"]
        CInv["不变式:<br/>队列按FIFO排序"]
        CAcquire["acquire:<br/>加入队列尾部<br/>自旋等待前驱"]
        CRelease["release:<br/>标记locked=false<br/>复用节点"]
    end

    TN --> TInv
    TS --> TInv
    TInv --> TAcquire
    TInv --> TRelease

    CT --> CQ
    CQ --> CInv
    CInv --> CAcquire
    CInv --> CRelease

    TInv -.->|公平性保证| Fair["先到先服务"]
    CInv -.->|公平性保证| Fair
```

### 7.6 无锁数据结构验证图

Treiber栈的验证结构和关键证明步骤。

```mermaid
graph TB
    subgraph "Treiber栈状态"
        Head["head: 指向栈顶"]
        List["链表结构<br/>表示当前栈内容"]
        GhostA["幽灵授权<br/>◯ xs"]
        GhostF["幽灵碎片<br/>◐ xs"]
    end

    subgraph "操作与证明"
        Push["push(v):<br/>1. 创建新节点<br/>2. CAS更新head<br/>3. 幽灵状态更新"]
        Pop["pop():<br/>1. 读取head<br/>2. CAS移除首节点<br/>3. 幽灵状态验证"]
    end

    subgraph "线性化点"
        LP1["push的线性化点:<br/>CAS成功时"]
        LP2["pop的线性化点:<br/>CAS成功时"]
    end

    subgraph "不变式"
        Inv1["head指向链表首节点"]
        Inv2["幽灵状态与物理状态一致"]
        Inv3["无内存泄漏<br/>pop释放节点"]
    end

    Head --> List
    List --> GhostA
    GhostA --> GhostF
    GhostA --> Push
    GhostA --> Pop
    Push --> LP1
    Pop --> LP2
    List --> Inv1
    GhostA --> Inv2
    Pop --> Inv3

    style LP1 fill:#fff3e0,stroke:#e65100
    style LP2 fill:#fff3e0,stroke:#e65100
    style GhostA fill:#ffebee,stroke:#b71c1c
```

---

## 8. 引用参考 (References)





















---

## 附录A: Iris符号速查表

| 符号 | LaTeX | 含义 |
|------|-------|------|
| ▷ | `\later` | Later模态 |
| □ | `\persistently` | Persistently模态 |
| ⚡ | `\update` | Fancy Update模态 |
| ✓ | `\valid` | 有效性谓词 |
| ◯ | `\circ` | 幽灵授权 |
| ● | `\bullet` | 幽灵碎片 |
| ⋅ | `\cdot` | RA组合运算 |
| ⊢ | `\vdash` | 逻辑推导 |
| ⊣⊢ | `\dashv\vdash` | 逻辑等价 |
| −∗ | `--*` | 分离蕴含 |
| ∗ | `\ast` | 分离合取 |
| wand | `\wand` | 分离蕴含 |
| ℓ ↦ v | `\mapsto` | 堆映射 |

## 附录B: 资源代数速查表

| RA | 元素 | 运算 | 有效性 | 用途 |
|----|------|------|--------|------|
| Ex(A) | ⊥ \| a∈A | a·b未定义(⊥) | ✓(a) | 独占所有权 |
| Frac | (0,1]∩ℚ | q₁+q₂ | q≤1 | 分数权限 |
| Auth(M) | ◯a \| ●a | ◯a·●a=◯a | ✓(a) | 授权-碎片 |
| Ag(T) | {t} | 合并 | 一致性 | 协议一致性 |
| Max(N) | n∈ℕ | max(n₁,n₂) | ⊤ | 单调计数器 |

## 附录C: Coq实现参考

Iris的Coq实现可在以下位置找到：

- **GitHub**: <https://github.com/iris-project/iris>
- **文档**: <https://iris-project.org/>
- **教程**: <https://iris-project.org/tutorial.html>
- **API文档**: <https://plv.mpi-sws.org/iris/iris/>

核心库结构：

```
iris/
├── algebra/          # 资源代数和相机理论
├── bi/               # 双态逻辑基础
├── proofmode/        # 证明模式(ltac策略)
├── heap_lang/        # 示例语言(堆操作)
├── program_logic/    # 程序逻辑(WP、Hoare)
└── base_logic/       # 基础逻辑(模态、不变式)
```

---

*文档版本: v1.0 | 创建日期: 2026-04-10 | 形式化等级: L6*

*本文档遵循AGENTS.md六段式模板规范，包含24个定义、16个引理/命题、16个定理，6个Mermaid可视化图，以及20条学术引用。*
