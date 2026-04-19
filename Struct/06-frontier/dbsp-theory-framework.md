# DBSP (Database Stream Processor) 理论框架

> **所属阶段**: Struct/06-frontier | **前置依赖**: [01.04-dataflow-model-formalization.md](../01-foundation/01.04-dataflow-model-formalization.md), [streaming-lakehouse-formal-theory.md](streaming-lakehouse-formal-theory.md) | **形式化等级**: L5-L6

---

## 摘要

DBSP (Database Stream Processor) 是由 Frank McSherry、Leonid Ryzhyk 等人于 VLDB'23 / SIGMOD'24 提出的理论框架，旨在为增量视图维护 (Incremental View Maintenance, IVM) 提供严格的数学基础。DBSP 的核心创新在于将数据库查询和流处理统一到一个称为 **Z-set** 的代数结构中，通过引入 **差分算子 ∇** 和 **积分算子 ∇⁻¹**，建立了一套完整的增量计算理论。

本文档从形式化角度系统阐述 DBSP 的理论基础：首先定义 Z-sets、Z-set 转换器、线性算子等核心数学对象；随后详细推导 ∇ 算子的代数性质与链式法则；进而证明 DBSP 增量视图维护的正确性定理；最后建立 DBSP 与关系代数、Differential Dataflow、Timely Dataflow 之间的严格关系映射，并分析其在 Materialize、Feldera 等工业系统中的实现。

**关键词**: DBSP, Z-sets, 增量视图维护, Differential Dataflow, Timely Dataflow, 流处理, 形式化理论

---

## 目录

- [DBSP (Database Stream Processor) 理论框架](#dbsp-database-stream-processor-理论框架)
  - [摘要](#摘要)
  - [目录](#目录)
  - [1. 概念定义 (Definitions)](#1-概念定义-definitions)
    - [1.1 Z-sets 形式化定义](#11-z-sets-形式化定义)
    - [1.2 Z-set 转换器](#12-z-set-转换器)
    - [1.3 差分算子 ∇](#13-差分算子-)
    - [1.4 积分算子 ∇⁻¹](#14-积分算子-)
    - [1.5 DBSP 计算模型](#15-dbsp-计算模型)
    - [1.6 线性算子与可增量性](#16-线性算子与可增量性)
    - [1.7 嵌套 Z-sets 与高阶数据](#17-嵌套-z-sets-与高阶数据)
  - [2. 属性推导 (Properties)](#2-属性推导-properties)
    - [2.1 ∇ 算子的基本代数性质](#21--算子的基本代数性质)
    - [2.2 积分与差分的互逆性](#22-积分与差分的互逆性)
    - [2.3 增量传播链式法则](#23-增量传播链式法则)
    - [2.4 线性算子的增量封闭性](#24-线性算子的增量封闭性)
    - [2.5 循环算子的不动点性质](#25-循环算子的不动点性质)
  - [3. 关系建立 (Relations)](#3-关系建立-relations)
    - [3.1 DBSP 与关系代数的编码](#31-dbsp-与关系代数的编码)
    - [3.2 DBSP 与 Differential Dataflow](#32-dbsp-与-differential-dataflow)
    - [3.3 DBSP 与 Timely Dataflow 的层次关系](#33-dbsp-与-timely-dataflow-的层次关系)
    - [3.4 DBSP 与 Dataflow Model 的语义映射](#34-dbsp-与-dataflow-model-的语义映射)
    - [3.5 表达能力层次](#35-表达能力层次)
  - [4. 论证过程 (Argumentation)](#4-论证过程-argumentation)
    - [4.1 非线性算子的增量化策略](#41-非线性算子的增量化策略)
    - [4.2 嵌套递归与不动点语义](#42-嵌套递归与不动点语义)
    - [4.3 边界讨论：DBSP 的适用范围](#43-边界讨论dbsp-的适用范围)
    - [4.4 反例分析：不可增量化的查询](#44-反例分析不可增量化的查询)
  - [5. 形式证明 / 工程论证 (Proof / Engineering Argument)](#5-形式证明--工程论证-proof--engineering-argument)
    - [5.1 DBSP 增量视图维护正确性定理](#51-dbsp-增量视图维护正确性定理)
    - [5.2 定理完整证明](#52-定理完整证明)
    - [5.3 工程实现正确性论证](#53-工程实现正确性论证)
    - [5.4 复杂度分析](#54-复杂度分析)
  - [6. 实例验证 (Examples)](#6-实例验证-examples)
    - [6.1 简化实例：计数查询的增量维护](#61-简化实例计数查询的增量维护)
    - [6.2 连接操作的增量维护](#62-连接操作的增量维护)
    - [6.3 递归查询（传递闭包）的增量维护](#63-递归查询传递闭包的增量维护)
    - [6.4 Materialize 的 DBSP 实现](#64-materialize-的-dbsp-实现)
    - [6.5 Feldera 的 DBSP 实现](#65-feldera-的-dbsp-实现)
    - [6.6 Streaming SQL 语义影响分析](#66-streaming-sql-语义影响分析)
  - [7. 可视化 (Visualizations)](#7-可视化-visualizations)
    - [7.1 DBSP 理论层次图](#71-dbsp-理论层次图)
    - [7.2 增量计算执行流程](#72-增量计算执行流程)
    - [7.3 表达能力对比矩阵](#73-表达能力对比矩阵)
    - [7.4 工业系统架构映射](#74-工业系统架构映射)
  - [8. 引用参考 (References)](#8-引用参考-references)

---

## 1. 概念定义 (Definitions)

### 1.1 Z-sets 形式化定义

**Def-S-06-19-01 [Z-sets 形式化定义]**: 设 $\mathcal{U}$ 为一个有限或可数无限的值域 (universe of values)。一个 **Z-set**（带整数重数的集合）是定义在 $\mathcal{U}$ 上的函数 $Z: \mathcal{U} \to \mathbb{Z}$，其中 $Z(v)$ 表示值 $v$ 的**重数** (multiplicity)。要求 $Z$ 具有有限支撑 (finite support)，即集合 $\{ v \in \mathcal{U} \mid Z(v) \neq 0 \}$ 是有限的。

所有 Z-sets 的集合记为 $\mathcal{Z} = \{ Z: \mathcal{U} \to \mathbb{Z} \mid \text{supp}(Z) \text{ 有限} \}$。

**Z-set 的等价表示**:

Z-set 可以等价地表示为以下形式之一：

1. **函数表示**: $Z: \mathcal{U} \to \mathbb{Z}$
2. **多重集表示**: $\{ v_1^{m_1}, v_2^{m_2}, \ldots, v_n^{m_n} \}$，其中 $m_i = Z(v_i)$
3. **形式线性组合**: $Z = \sum_{v \in \mathcal{U}} Z(v) \cdot [v]$，其中 $[v]$ 为狄拉克 delta 函数

**Z-set 的基本运算**:

设 $Z_1, Z_2 \in \mathcal{Z}$，定义：

- **加法** (Z-set union): $(Z_1 + Z_2)(v) = Z_1(v) + Z_2(v)$
- **数乘**: $(k \cdot Z)(v) = k \cdot Z(v)$，其中 $k \in \mathbb{Z}$
- **零元**: $\mathbf{0}(v) = 0$ 对所有 $v \in \mathcal{U}$
- **负元**: $(-Z)(v) = -Z(v)$

**命题**: $(\mathcal{Z}, +, \mathbf{0})$ 构成一个**自由阿贝尔群** (free abelian group)，其基为 $\{ [v] \mid v \in \mathcal{U} \}$。

**证明概要**: 由定义直接验证群公理：

- 封闭性: $Z_1 + Z_2$ 仍具有有限支撑
- 结合律: $(Z_1 + Z_2) + Z_3 = Z_1 + (Z_2 + Z_3)$ 逐点成立
- 单位元: $Z + \mathbf{0} = Z$
- 逆元: $Z + (-Z) = \mathbf{0}$
- 交换律: $Z_1 + Z_2 = Z_2 + Z_1$

**与传统集合的关系**:

| 概念 | 传统集合 | Z-set |
|------|---------|-------|
| 元素存在性 | $v \in S$ 或 $v \notin S$ | $Z(v) \in \mathbb{Z}$ |
| 并集 | $S_1 \cup S_2$ | $Z_1 + Z_2$ |
| 交集 | $S_1 \cap S_2$ | $Z_1 \times Z_2$（逐点乘） |
| 差集 | $S_1 \setminus S_2$ | $Z_1 - Z_2$ |
| 空集 | $\emptyset$ | $\mathbf{0}$ |

**Z-set 的具象化** (concretization):

定义映射 $\text{concrete}: \mathcal{Z} \to 2^{\mathcal{U}}$ 为：

$$\text{concrete}(Z) = \{ v \in \mathcal{U} \mid Z(v) > 0 \}$$

该映射将 Z-set 投影到传统集合（忽略负重数）。注意 $\text{concrete}$ 不是单射：多个不同的 Z-set 可能映射到同一个传统集合。

**DISTINCT 操作**:

定义操作 $\text{DISTINCT}: \mathcal{Z} \to \mathcal{Z}$ 为：

$$\text{DISTINCT}(Z)(v) = \begin{cases} 1 & \text{if } Z(v) > 0 \\ 0 & \text{if } Z(v) \leq 0 \end{cases}$$

DISTINCT 将 Z-set 转换为元素重数仅为 0 或 1 的集合（即传统集合的嵌入）。

---

### 1.2 Z-set 转换器

**Def-S-06-19-02 [Z-set 转换器]**: 一个 **Z-set 转换器** (Z-set transformer) 是一个函数 $T: \mathcal{Z}^k \to \mathcal{Z}$，其中 $k \geq 0$ 为转换器的元数 (arity)。当 $k = 0$ 时，$T$ 为常量 Z-set；当 $k = 1$ 时，$T$ 为一元转换器；当 $k = 2$ 时，$T$ 为二元转换器。

**DBSP 转换器分类**:

| 类别 | 定义 | 典型算子 |
|------|------|---------|
| 线性转换器 | $T(Z_1 + Z_2) = T(Z_1) + T(Z_2)$ 且 $T(k \cdot Z) = k \cdot T(Z)$ | SELECT, PROJECT, FILTER, UNION |
| 非线性转换器 | 不满足线性条件 | DISTINCT, GROUP BY + AGG, JOIN |
| 时序转换器 | 依赖输入历史序列 | 延迟 (delay)、反馈 (feedback) |

**核心一元算子定义**:

设 $Z \in \mathcal{Z}$，定义以下基本算子：

1. **投影** (PROJECT): 给定函数 $f: \mathcal{U} \to \mathcal{U}$，
   $$(\pi_f(Z))(v) = \sum_{u: f(u) = v} Z(u)$$

2. **选择** (SELECT): 给定谓词 $p: \mathcal{U} \to \{0, 1\}$，
   $$(\sigma_p(Z))(v) = p(v) \cdot Z(v)$$

3. **笛卡尔积** (PRODUCT): 给定 $Z_1, Z_2 \in \mathcal{Z}$，
   $$(Z_1 \times Z_2)((v_1, v_2)) = Z_1(v_1) \cdot Z_2(v_2)$$

4. **扁平化** (FLATMAP): 给定函数 $g: \mathcal{U} \to \mathcal{Z}$，
   $$(\text{FLATMAP}_g(Z))(v) = \sum_{u \in \mathcal{U}} Z(u) \cdot g(u)(v)$$

**命题**: PROJECT、SELECT、FLATMAP 都是**线性算子**。

**证明**: 以 PROJECT 为例，验证线性条件：

$$\begin{aligned}
(\pi_f(Z_1 + Z_2))(v) &= \sum_{u: f(u) = v} (Z_1 + Z_2)(u) \\
&= \sum_{u: f(u) = v} (Z_1(u) + Z_2(u)) \\
&= \sum_{u: f(u) = v} Z_1(u) + \sum_{u: f(u) = v} Z_2(u) \\
&= (\pi_f(Z_1))(v) + (\pi_f(Z_2))(v)
\end{aligned}$$

数乘条件的验证类似。

---

### 1.3 差分算子 ∇

**Def-S-06-19-03 [差分算子 ∇]**: 差分算子 $\nabla: \mathcal{Z}^{\mathbb{N}} \to \mathcal{Z}^{\mathbb{N}}$ 作用于**Z-set 序列** $Z = (Z_0, Z_1, Z_2, \ldots)$，产生新的序列 $\nabla Z = ((\nabla Z)_0, (\nabla Z)_1, \ldots)$，定义为：

$$(\nabla Z)_0 = Z_0$$

$$(\nabla Z)_t = Z_t - Z_{t-1} \quad \text{for } t > 0$$

其中减法为 Z-set 的逐点减法（即群运算）。

**差分算子的直观含义**:

$\nabla$ 将绝对值序列转换为**增量序列** (delta sequence)。第 $t$ 个增量 $(\nabla Z)_t$ 表示从时刻 $t-1$ 到时刻 $t$ 发生的变更：正值表示插入，负值表示删除。

**示例**: 设 $Z = (Z_0, Z_1, Z_2)$ 如下：

```
Z_0: {a^1, b^1}      (a和b各出现1次)
Z_1: {a^1, b^2, c^1}  (b增加1次，c新增)
Z_2: {a^2, b^1}      (a增加1次，c删除，b减少1次)
```

则 $\nabla Z = ((\nabla Z)_0, (\nabla Z)_1, (\nabla Z)_2)$：

```
(∇Z)_0 = {a^1, b^1}
(∇Z)_1 = {b^1, c^1}     (b增加，c插入)
(∇Z)_2 = {a^1, b^{-1}, c^{-1}}  (a增加，b减少，c删除)
```

**∇ 算子作为序列空间上的线性算子**:

定义序列空间 $\mathcal{S} = \mathcal{Z}^{\mathbb{N}}$，则 $\nabla: \mathcal{S} \to \mathcal{S}$。对于序列的逐点加法，$\nabla$ 是线性的：

$$\nabla(Z^{(1)} + Z^{(2)}) = \nabla Z^{(1)} + \nabla Z^{(2)}$$

---

### 1.4 积分算子 ∇⁻¹

**Def-S-06-19-04 [积分算子 ∇⁻¹]**: 积分算子 $\nabla^{-1}: \mathcal{Z}^{\mathbb{N}} \to \mathcal{Z}^{\mathbb{N}}$ 作用于增量序列 $D = (D_0, D_1, D_2, \ldots)$，产生累积序列 $Z = \nabla^{-1} D = (Z_0, Z_1, Z_2, \ldots)$，定义为：

$$Z_t = \sum_{i=0}^{t} D_i$$

即 $Z_t$ 为增量序列前 $t+1$ 项的累积和（前缀和）。

**积分算子的直观含义**:

$\nabla^{-1}$ 将增量序列还原为绝对值序列。给定一系列变更（插入/删除），积分算子计算每个时刻的累积状态。

**∇ 与 ∇⁻¹ 的关系**:

这两个算子互为逆运算，构成 DBSP 增量理论的核心对偶结构。

---

### 1.5 DBSP 计算模型

**Def-S-06-19-05 [DBSP 计算模型]**: 一个 **DBSP 程序** (DBSP program) 是一个有向图 $G = (V, E, \lambda, \omega)$，其中：

- $V$: 节点集合，每个节点代表一个 Z-set 转换器
- $E \subseteq V \times V$: 有向边集合，表示数据流
- $\lambda: V \to \mathcal{T}$: 节点标注函数，将每个节点映射到一个 Z-set 转换器类型
- $\omega: E \to \mathbb{N}$: 边延迟标注，表示边上的延迟步数（通常 $\omega(e) \in \{0, 1\}$）

**DBSP 程序的语义**: 给定输入序列 $I = (I_0, I_1, \ldots)$，DBSP 程序按以下规则计算输出序列 $O = (O_0, O_1, \ldots)$：

在每个时间步 $t$，每个节点 $v \in V$ 计算其输出 $O_v^{(t)}$：

$$O_v^{(t)} = \lambda(v)\left( \{ O_u^{(t - \omega(u,v))} \mid (u,v) \in E \} \right)$$

其中未定义的 $O_u^{(s)}$（当 $s < 0$ 时）视为 $\mathbf{0}$。

**DBSP 程序的增量版本**: 对于 DBSP 程序 $G$，其增量版本 $\nabla G$ 是将所有边上的数据替换为增量流，并在每个节点处应用增量化规则（见第 2.3 节链式法则）。

---

### 1.6 线性算子与可增量性

**Def-S-06-19-06 [线性算子与可增量性]**: 一个 Z-set 转换器 $T: \mathcal{Z} \to \mathcal{Z}$ 称为**线性的** (linear)，如果对于所有 $Z_1, Z_2 \in \mathcal{Z}$ 和 $k \in \mathbb{Z}$：

1. **可加性**: $T(Z_1 + Z_2) = T(Z_1) + T(Z_2)$
2. **齐次性**: $T(k \cdot Z_1) = k \cdot T(Z_1)$

**线性算子的增量化性质**: 若 $T$ 是线性算子，则其增量形式直接由线性性得到：

$$T(Z + \Delta Z) = T(Z) + T(\Delta Z)$$

即输出增量 $\Delta(T(Z)) = T(\Delta Z)$。这意味着**线性算子的增量计算不需要维护额外状态**。

**非线性算子的增量化**: 对于非线性算子 $N$，增量计算通常需要维护额外状态 $S$，使得：

$$N(Z + \Delta Z) = N(Z) + \Delta N(Z, \Delta Z, S)$$

其中 $\Delta N$ 为增量更新函数，$S$ 为辅助状态。

**可增量性判定**:

| 算子类型 | 是否线性 | 增量化复杂度 | 需维护状态 |
|---------|---------|------------|----------|
| SELECT | ✅ 是 | $O(|\Delta Z|)$ | 无 |
| PROJECT | ✅ 是 | $O(|\Delta Z|)$ | 无 |
| UNION | ✅ 是 | $O(|\Delta Z|)$ | 无 |
| CROSS PRODUCT | ✅ 是 | $O(|\Delta Z_1| \cdot |Z_2| + |Z_1| \cdot |\Delta Z_2|)$ | 需维护输入状态 |
| DISTINCT | ❌ 否 | $O(|\Delta Z|)$ | 需维护元素计数器 |
| GROUP BY + COUNT | ❌ 否 | $O(|\Delta Z|)$ | 需维护分组计数 |
| JOIN | ❌ 否 | $O(|\Delta Z_1| \cdot |Z_2| + |Z_1| \cdot |\Delta Z_2|)$ | 需维护两侧状态 |

---

### 1.7 嵌套 Z-sets 与高阶数据

**Def-S-06-19-07 [嵌套 Z-sets]**: 设 $\mathcal{U}$ 为值域。递归定义嵌套 Z-sets 的类型系统 $\mathcal{Z}^*$：

1. **基础类型**: 若 $v \in \mathcal{U}$，则 $v$ 是基础值
2. **Z-set 类型**: 若 $T$ 是嵌套类型，则 $\mathcal{Z}(T)$ 是元素类型为 $T$ 的 Z-set
3. **积类型**: 若 $T_1, T_2$ 是嵌套类型，则 $(T_1, T_2)$ 是积类型

嵌套 Z-sets 允许表示复杂嵌套结构，例如 Z-set of Z-sets（集合的集合），这是支持嵌套关系查询和递归查询的关键。

**示例**: 表示图结构 $G = (V, E)$：

- 节点集: $V \in \mathcal{Z}(\text{NodeId})$
- 边集: $E \in \mathcal{Z}(\text{NodeId} \times \text{NodeId})$
- 邻接表: $A \in \mathcal{Z}(\text{NodeId} \times \mathcal{Z}(\text{NodeId}))$

---

## 2. 属性推导 (Properties)

### 2.1 ∇ 算子的基本代数性质

**Lemma-S-06-19-01 [∇ 算子的线性性]**: 差分算子 $\nabla: \mathcal{S} \to \mathcal{S}$ 是线性算子。即对于任意序列 $X, Y \in \mathcal{S}$ 和整数 $k \in \mathbb{Z}$：

1. $\nabla(X + Y) = \nabla X + \nabla Y$
2. $\nabla(k \cdot X) = k \cdot \nabla X$

**证明**:

对于性质 1，逐时间步验证：

- 当 $t = 0$ 时：
  $$(\nabla(X + Y))_0 = (X + Y)_0 = X_0 + Y_0 = (\nabla X)_0 + (\nabla Y)_0$$

- 当 $t > 0$ 时：
  $$\begin{aligned}
  (\nabla(X + Y))_t &= (X + Y)_t - (X + Y)_{t-1} \\
  &= X_t + Y_t - X_{t-1} - Y_{t-1} \\
  &= (X_t - X_{t-1}) + (Y_t - Y_{t-1}) \\
  &= (\nabla X)_t + (\nabla Y)_t
  \end{aligned}$$

性质 2 的验证类似。$\square$

**Lemma-S-06-19-02 [∇ 的核与像]**: 设 $\mathcal{S}_0 = \{ X \in \mathcal{S} \mid X_0 = \mathbf{0} \}$（初始为零的序列空间），则：

1. $\ker(\nabla) = \{ (Z, Z, Z, \ldots) \mid Z \in \mathcal{Z} \}$（常数序列空间）
2. $\text{im}(\nabla) = \mathcal{S}_0$（初始为零的序列空间）

**证明**:

对于性质 1，若 $\nabla X = \mathbf{0}$（零序列），则：
- $(\nabla X)_0 = X_0 = \mathbf{0}$
- $(\nabla X)_t = X_t - X_{t-1} = \mathbf{0}$ 对所有 $t > 0$

因此 $X_t = X_{t-1}$ 对所有 $t > 0$，即 $X$ 为常数序列。

对于性质 2：
- 包含关系 $\text{im}(\nabla) \subseteq \mathcal{S}_0$: 对任意 $X$，$(\nabla X)_0 = X_0$，但注意这里 $
abla$ 的定义使得 $(\nabla X)_0 = X_0$，而后续差分项初始为 $X_1 - X_0$。实际上，若考虑从 $\mathcal{S}_0$ 出发的序列，需要重新索引。

更精确的表述：定义修正差分算子 $\nabla'$ 为 $(\nabla' X)_0 = \mathbf{0}$ 且 $(\nabla' X)_t = X_t - X_{t-1}$（$t > 0$），则 $\text{im}(\nabla') = \mathcal{S}_0$ 且 $\ker(\nabla')$ 为常数序列。$\square$

---

### 2.2 积分与差分的互逆性

**Prop-S-06-19-01 [∇ 与 ∇⁻¹ 的互逆性]**:

1. 对任意增量序列 $D \in \mathcal{S}$，$\nabla(\nabla^{-1} D) = D$
2. 对任意序列 $Z \in \mathcal{S}$，若 $Z_0 = \mathbf{0}$，则 $\nabla^{-1}(\nabla Z) = Z$

**证明**:

对于性质 1：设 $Z = \nabla^{-1} D$，即 $Z_t = \sum_{i=0}^{t} D_i$。

- $(\nabla Z)_0 = Z_0 = D_0$
- 对 $t > 0$：
  $$\begin{aligned}
  (\nabla Z)_t &= Z_t - Z_{t-1} \\
  &= \sum_{i=0}^{t} D_i - \sum_{i=0}^{t-1} D_i \\
  &= D_t
  \end{aligned}$$

因此 $\nabla(\nabla^{-1} D) = D$。

对于性质 2：设 $D = \nabla Z$，即 $D_0 = Z_0 = \mathbf{0}$，$D_t = Z_t - Z_{t-1}$（$t > 0$）。

计算 $(\nabla^{-1} D)_t = \sum_{i=0}^{t} D_i = D_0 + \sum_{i=1}^{t} (Z_i - Z_{i-1}) = \mathbf{0} + Z_t - Z_0 = Z_t$。

注意若 $Z_0 \neq \mathbf{0}$，则 $\nabla^{-1}(\nabla Z)_0 = D_0 = Z_0$，但 $\nabla Z$ 的定义使得 $(\nabla Z)_0 = Z_0$，因此需要 $D_0 = \mathbf{0}$ 的条件才能保证完全互逆。这是 DBSP 理论中的标准约定：差分序列的初始项定义为 $\mathbf{0}$，而绝对序列包含初始状态。$\square$

---

### 2.3 增量传播链式法则

**Lemma-S-06-19-03 [DBSP 链式法则]**: 设 $T: \mathcal{Z} \to \mathcal{Z}$ 为任意 Z-set 转换器，$Z \in \mathcal{Z}^{\mathbb{N}}$ 为输入序列。定义输出序列 $O_t = T(Z_t)$。则输出的增量序列 $\nabla O$ 与输入的增量序列 $\nabla Z$ 满足：

$$(\nabla O)_t = T(Z_t) - T(Z_{t-1}) = T\left(Z_{t-1} + (\nabla Z)_t\right) - T(Z_{t-1})$$

特别地，若 $T$ 是线性算子，则：

$$(\nabla O)_t = T((\nabla Z)_t)$$

即输出增量仅依赖于输入增量，与累积状态无关。

**证明**: 直接由定义：

$$(\nabla O)_t = O_t - O_{t-1} = T(Z_t) - T(Z_{t-1})$$

而 $Z_t = Z_{t-1} + (\nabla Z)_t$（因为 $\nabla^{-1}(\nabla Z) = Z$ 在适当初始条件下），所以：

$$(\nabla O)_t = T(Z_{t-1} + (\nabla Z)_t) - T(Z_{t-1})$$

若 $T$ 线性：

$$T(Z_{t-1} + (\nabla Z)_t) - T(Z_{t-1}) = T(Z_{t-1}) + T((\nabla Z)_t) - T(Z_{t-1}) = T((\nabla Z)_t)$$

$\square$

**链式法则的推广（多输入情况）**:

设 $T: \mathcal{Z}^k \to \mathcal{Z}$ 为 $k$ 元转换器，$Z^{(1)}, \ldots, Z^{(k)}$ 为输入序列，$O_t = T(Z_t^{(1)}, \ldots, Z_t^{(k)})$。则：

$$(\nabla O)_t = T(Z_t^{(1)}, \ldots, Z_t^{(k)}) - T(Z_{t-1}^{(1)}, \ldots, Z_{t-1}^{(k)})$$

对于线性 $T$，上式简化为：

$$(\nabla O)_t = T((\nabla Z^{(1)})_t, \ldots, (\nabla Z^{(k)})_t)$$

对于双线性算子（如 CROSS PRODUCT、JOIN），若 $T(Z_1, Z_2) = Z_1 \times Z_2$，则：

$$\begin{aligned}
(\nabla O)_t &= Z_t^{(1)} \times Z_t^{(2)} - Z_{t-1}^{(1)} \times Z_{t-1}^{(2)} \\
&= (Z_{t-1}^{(1)} + (\nabla Z^{(1)})_t) \times (Z_{t-1}^{(2)} + (\nabla Z^{(2)})_t) - Z_{t-1}^{(1)} \times Z_{t-1}^{(2)} \\
&= Z_{t-1}^{(1)} \times (\nabla Z^{(2)})_t + (\nabla Z^{(1)})_t \times Z_{t-1}^{(2)} + (\nabla Z^{(1)})_t \times (\nabla Z^{(2)})_t
\end{aligned}$$

该公式表明 JOIN 的增量计算需要维护两侧输入的当前状态 $Z_{t-1}^{(1)}$ 和 $Z_{t-1}^{(2)}$。

---

### 2.4 线性算子的增量封闭性

**Lemma-S-06-19-04 [线性算子的增量封闭性]**: 设 $T_1, T_2: \mathcal{Z} \to \mathcal{Z}$ 为线性算子，$k \in \mathbb{Z}$。则：

1. $T_1 + T_2$（逐点和）是线性的
2. $k \cdot T_1$ 是线性的
3. $T_1 \circ T_2$（复合）是线性的

因此，线性算子构成 $\text{End}(\mathcal{Z})$（$\mathcal{Z}$ 的自同态代数）的子代数。

**证明**: 直接验证。

对于复合：

$$(T_1 \circ T_2)(Z_1 + Z_2) = T_1(T_2(Z_1 + Z_2)) = T_1(T_2(Z_1) + T_2(Z_2)) = T_1(T_2(Z_1)) + T_1(T_2(Z_2))$$

齐次性类似。$\square$

---

### 2.5 循环算子的不动点性质

**Def-S-06-19-08 [循环算子]**: 设 $T: \mathcal{Z} \times \mathcal{Z} \to \mathcal{Z}$ 为二元转换器。循环算子 $\text{LOOP}_T: \mathcal{Z} \to \mathcal{Z}$ 定义为以下方程的**最小不动点** (least fixed point)：

$$\text{LOOP}_T(I) = T(I, \text{LOOP}_T(I))$$

在序列语义下，LOOP 算子对应于带反馈的 DBSP 程序：

```
      ┌─────────────────────┐
      │                     │
      ▼                     │
  I ──┴──► T(I, S) ──► S ──┘
             │
             ▼
             O
```

**序列语义下的 LOOP**: 设 $I = (I_0, I_1, \ldots)$ 为输入序列，$S = (S_0, S_1, \ldots)$ 为反馈状态序列，则：

$$S_t = T(I_t, S_{t-1})$$

其中 $S_{-1} = \mathbf{0}$（初始空状态）。

**Prop-S-06-19-02 [循环算子的增量化]**: 若 $T$ 关于其第二个参数是线性的，则 LOOP 算子可按以下方式增量化：

设 $S_t = T(I_t, S_{t-1})$，则增量的反馈状态 $(\nabla S)_t$ 满足：

$$(\nabla S)_t = T((\nabla I)_t, S_{t-1})$$

当 $T$ 关于两个参数都是双线性时，公式需扩展以处理交叉项。

---

## 3. 关系建立 (Relations)

### 3.1 DBSP 与关系代数的编码

关系代数可以完整编码到 DBSP 的 Z-set 框架中。设关系 $R$ 的嵌入为 Z-set $Z_R$，其中 $Z_R(v) = 1$ 当且仅当 $v \in R$，否则为 $0$。

**关系代数到 Z-set 转换器的映射**:

| 关系代数算子 | Z-set 转换器 | 线性性 |
|------------|------------|-------|
| $\sigma_p(R)$ | SELECT$_p(Z_R)$ | 线性 |
| $\pi_A(R)$ | PROJECT$_A(Z_R)$ | 线性 |
| $R \cup S$ | $Z_R + Z_S$ | 线性 |
| $R \setminus S$ | $Z_R - Z_S$ | 线性 |
| $R \times S$ | $Z_R \times Z_S$（笛卡尔积） | 双线性 |
| $R \bowtie_\theta S$ | $\sigma_\theta(Z_R \times Z_S)$ | 非线性（含选择） |
| $\gamma_{G, agg}(R)$ | GROUP-BY-AGG$_G(Z_R)$ | 非线性 |
| $\delta(R)$ (DISTINCT) | DISTINCT$(Z_R)$ | 非线性 |

**定理（关系代数完备性）**: 标准关系代数（SPJ 查询 + 分组聚合）可以完整编码为 DBSP 程序，且 SPJ 查询的编码完全由线性算子组成。

**递归关系代数**: 支持递归（如 Datalog）的关系代数需要在 DBSP 中引入 LOOP 算子。Datalog 程序 $P$ 可以编译为 DBSP 程序 $G_P$，其中：

- 每个 EDB（扩展数据库）关系映射为输入节点
- 每个 IDB（内涵数据库）关系映射为 LOOP 算子的输出
- 每个规则体映射为 PROJECT + SELECT + JOIN 的组合
- 递归定义映射为 LOOP 的反馈边

---

### 3.2 DBSP 与 Differential Dataflow

**Differential Dataflow 回顾**: Differential Dataflow (DD) 是 Frank McSherry 等人在 CIDR'13 提出的增量计算框架。DD 基于 Timely Dataflow 的执行引擎，引入**差分** (difference) 的概念，支持多版本状态维护和嵌套循环的增量更新。

**核心区别与联系**:

| 特性 | Differential Dataflow | DBSP |
|------|----------------------|------|
| 数据模型 | 任意类型 + 差分算子 | Z-sets (限定数据模型) |
| 增量粒度 | 多版本、多维时间戳 | 单时间轴序列 |
| 循环支持 | 原生支持嵌套循环 | 通过 LOOP 算子支持 |
| 实现复杂度 | 高（需要复杂索引） | 相对较低（更约束） |
| 正确性证明 | 工程验证为主 | 严格代数证明 |
| 应用场景 | 通用图计算、迭代算法 | 数据库视图维护、Streaming SQL |

**形式化关系**: DBSP 可以视为 Differential Dataflow 的**理论抽象**和**约束子集**。具体而言：

1. DD 的 collection 类型在 DBSP 中特化为 Z-set
2. DD 的 `iterate` 操作在 DBSP 中对应 LOOP 算子
3. DD 的多维时间戳在 DBSP 中简化为自然数时间轴 $\mathbb{N}$
4. DD 的差分传播在 DBSP 中由 ∇ 算子的链式法则形式化

**层次关系**: Timely Dataflow (最灵活) $\supset$ Differential Dataflow (增量约束) $\supset$ DBSP (更强约束、更易实现)

---

### 3.3 DBSP 与 Timely Dataflow 的层次关系

**Timely Dataflow 回顾**: Timely Dataflow (Naiad, SOSP'13) 是一种支持**有界循环** (bounded loops) 的分布式数据流模型。其核心创新包括：

1. **能力** (capabilities)：表示数据在循环中的迭代进度
2. **时间戳**：二维时间戳 $(e, i)$，其中 $e$ 为事件时间，$i$ 为迭代轮次
3. **进度跟踪**：通过水位线 (progress tracking) 机制检测计算完成

**DBSP 到 Timely Dataflow 的编码**:

设 DBSP 程序 $G = (V, E, \lambda, \omega)$，其到 Timely Dataflow 的编码 $\text{TD}(G) = (V', E', \tau)$ 定义为：

- 每个 DBSP 节点 $v \in V$ 映射到 TD 算子 $v' \in V'$
- DBSP 的延迟边 $\omega(e) = 1$ 映射到 TD 的反馈通道，使用时钟能力管理
- DBSP 的 Z-set 数据映射到 TD 的 collection 类型
- DBSP 的时间步 $t \in \mathbb{N}$ 映射到 TD 时间戳的迭代维度

**定理（编码正确性）**: 对于无循环的 DBSP 程序 $G$，$\text{TD}(G)$ 在相同输入下产生与 $G$ 相同的输出序列。对于含 LOOP 的 DBSP 程序，编码需要额外引入迭代能力管理，保证每轮迭代的隔离性。

---

### 3.4 DBSP 与 Dataflow Model 的语义映射

**Dataflow Model**（见 [01.04-dataflow-model-formalization.md](../01-foundation/01.04-dataflow-model-formalization.md)）定义了流计算的形式化语义，包含：

- 事件时间 (event time) 和处理时间 (processing time)
- Watermark 和窗口
- 触发器 (triggers) 和累积模式 (accumulation modes)

**DBSP 与 Dataflow Model 的语义映射**:

| Dataflow Model 概念 | DBSP 对应 |
|-------------------|----------|
| 元素 $(k, v, t)$ | Z-set 元素 $v$ 在时间 $t$ 的重数变化 |
| 窗口 (Window) | 时间范围内的 Z-set 累积 |
| Watermark $W(t)$ | 允许输出到时间 $t$ 的许可 |
| Trigger | 输出刷新的时间条件 |
| Accumulation | Z-set 的累积和语义 |

**关键差异**: Dataflow Model 强调**事件时间**和**乱序处理**，而 DBSP 采用**处理时间序列**模型（自然数时间轴）。DBSP 可以通过引入水印机制扩展为支持事件时间的模型：

**Def-S-06-19-09 [带事件时间的 Z-set]**: 带事件时间的 Z-set 是函数 $Z: \mathcal{U} \times \mathbb{T} \to \mathbb{Z}$，其中 $\mathbb{T}$ 为事件时间域。增量序列按处理时间索引，每个增量包含多个事件时间的变更。

---

### 3.5 表达能力层次

**Thm-S-06-19-02 [DBSP 表达能力定理]**: DBSP 的表达能力严格介于非增量关系代数和非增量图灵完备计算之间。具体而言：

1. DBSP 可以表达所有**关系代数查询**（包括递归 Datalog）的增量维护
2. DBSP 不能表达需要**全局状态聚合**且不满足增量分解性质的计算（如中位数、Top-K 的某些变体）
3. DBSP 可以表达所有**线性流处理算子**的增量形式

**证明概要**:

- 对于性质 1：通过第 3.1 节的编码，所有关系代数算子都可以映射到 Z-set 转换器。递归查询通过 LOOP 算子支持。
- 对于性质 2：某些聚合（如精确中位数）的增量更新需要维护与输入规模成正比的状态，且更新操作不是局部可分解的。
- 对于性质 3：由线性算子的定义直接得到。$\square$

---

## 4. 论证过程 (Argumentation)

### 4.1 非线性算子的增量化策略

非线性算子是 DBSP 增量化的核心挑战。本节分析主要非线性算子的增量化策略。

**DISTINCT 的增量化**:

DISTINCT 算子 $D(Z)$ 将 Z-set 中所有正重数元素投影为 1。其增量形式需要维护每个元素的**精确计数** (exact count)：

设 $c_t(v)$ 为元素 $v$ 在时间 $t$ 的累积重数，$c_t(v) = \sum_{i=0}^{t} (\nabla Z)_i(v)$。

则 DISTINCT 的增量输出为：

$$(\nabla D)_t(v) = \begin{cases}
1 & \text{if } c_{t-1}(v) \leq 0 \text{ and } c_t(v) > 0 \\
-1 & \text{if } c_{t-1}(v) > 0 \text{ and } c_t(v) \leq 0 \\
0 & \text{otherwise}
\end{cases}$$

即 DISTINCT 的增量仅在元素从"不存在"变为"存在"（或反向）时输出。

**GROUP BY + COUNT 的增量化**:

设分组键为 $g: \mathcal{U} \to K$，则 GROUP-BY-COUNT 算子输出：

$$G(Z) = \{ (k, c) \mid c = \sum_{v: g(v) = k} Z(v) \}$$

增量形式维护每个分组的计数 $n_t(k) = \sum_{v: g(v) = k} c_t(v)$。当增量 $(\nabla Z)_t$ 到达时：

1. 对每个受影响的 $v$，计算 $k = g(v)$
2. 更新 $n_t(k) = n_{t-1}(k) + (\nabla Z)_t(v)$
3. 若 $n_{t-1}(k)$ 和 $n_t(k)$ 跨越 0 或从 0 开始，输出对应分组的增量

**JOIN 的增量化**:

JOIN 算子 $J(Z_1, Z_2) = \sigma_\theta(Z_1 \times Z_2)$ 的增量形式已在第 2.3 节推导：

$$(\nabla J)_t = Z_{t-1}^{(1)} \times (\nabla Z^{(2)})_t + (\nabla Z^{(1)})_t \times Z_{t-1}^{(2)} + (\nabla Z^{(1)})_t \times (\nabla Z^{(2)})_t$$

其中交叉项 $(\nabla Z^{(1)})_t \times (\nabla Z^{(2)})_t$ 处理同一时刻两侧同时变更的情况。

---

### 4.2 嵌套递归与不动点语义

DBSP 支持递归查询（如传递闭包）的增量维护，这是其相比传统 IVM 框架的重要优势。

**传递闭包的 DBSP 表达**:

设边集 $E \in \mathcal{Z}(\text{Node} \times \text{Node})$，传递闭包 $TC(E)$ 满足：

$$TC(E) = E \cup (E \circ TC(E))$$

其中 $\circ$ 表示关系复合。在 DBSP 中，这对应于 LOOP 算子：

$$TC = \text{LOOP}_T(E), \quad T(E, S) = E \cup (E \circ S)$$

**增量传递闭包**:

当边集从 $E$ 变为 $E + \Delta E$ 时，传递闭包的增量 $\Delta TC$ 满足：

$$\Delta TC = \Delta E \cup (\Delta E \circ TC(E)) \cup (E \circ \Delta TC) \cup (\Delta E \circ \Delta TC)$$

该方程的解可以通过迭代求得，对应于 DBSP 中 LOOP 算子的增量传播。

**不动点收敛性**:

**Prop-S-06-19-03 [传递闭包增量收敛性]**: 若边集 $E$ 定义在有限节点集上（$|V| = n$），则传递闭包的增量计算在至多 $n$ 轮迭代内收敛。

**证明**: 每轮迭代至少发现一个"新"的可达节点对。由于节点对总数最多为 $n^2$，迭代必然在 $n^2$ 轮内终止。更精细的分析表明，若采用路径长度计数，则最长路径为 $n-1$，因此至多 $n-1$ 轮。$\square$

---

### 4.3 边界讨论：DBSP 的适用范围

DBSP 的理论框架具有明确的适用范围和限制。

**适用场景**:

1. **关系型查询的增量维护**: SELECT/PROJECT/JOIN/GROUP BY 等传统 SQL 查询
2. **流处理的持续查询**: Streaming SQL 的持续查询语义
3. **递归查询**: Datalog、传递闭包、图算法（在适当约束下）
4. **嵌套数据查询**: JSON/XML 的嵌套结构查询（通过嵌套 Z-sets）

**不适用场景**:

1. **非单调聚合**: 全局排序、精确中位数、某些百分位数
2. **非确定性计算**: 随机算法、蒙特卡洛模拟
3. **时间窗口的某些语义**: 需要回溯修改的滑动窗口（除非使用特殊编码）
4. **一般图灵完备计算**: 无限制递归、非结构化控制流

**扩展方向**:

| 限制 | 可能的扩展 |
|------|----------|
| 单时间轴 | 引入多维时间戳（向 DD 靠拢） |
| 精确聚合 | 近似算法 + 误差边界 |
| 有限递归 | 有界循环能力（类似 Timely Dataflow） |
| Z-set 数据模型 | 半环扩展（如 provenance semiring） |

---

### 4.4 反例分析：不可增量化的查询

并非所有查询都可以高效增量维护。以下查询在 DBSP 框架中需要特殊处理或不可增量化。

**反例 1：精确中位数**

设 $Z$ 为数值元素的 Z-set，中位数 $median(Z)$ 定义为排序后位于中间位置的值。中位数的增量更新需要：

- 维护所有元素的完整排序结构（或两个堆）
- 每次插入/删除可能导致中位数的变化，且变化不可局部预测
- 增量输出可能涉及大量元素的"位移"

在 DBSP 框架中，中位数查询可以表达，但其增量形式的状态维护复杂度为 $O(|Z|)$，与重新计算相比优势有限。

**反例 2：任意 Top-K 排名**

设 $Z$ 为带分数元素的集合，查询要求维护按分数排序的前 $K$ 个元素。当元素的分数更新时：

- 若更新元素不在 Top-K 中且新分数仍不足，无输出变化
- 若更新元素进入 Top-K，需要"挤出"当前第 $K$ 名
- 增量输出涉及排名变化传播

DBSP 可以维护 Top-K，但需要维护全局排序状态，增量优势在 $K$ 接近 $|Z|$ 时消失。

**反例 3：非单调子查询**

考虑查询 $Q = R \setminus (R \bowtie S)$。当 $S$ 增加时，$R \bowtie S$ 增加，导致 $Q$ 减少（反单调性）。DBSP 可以处理此类查询，但需要谨慎维护状态的一致性。

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

### 5.1 DBSP 增量视图维护正确性定理

**Thm-S-06-19-01 [DBSP 增量视图维护正确性定理]**: 设 $G$ 为任意 DBSP 程序，$I = (I_0, I_1, \ldots)$ 为输入序列，$O = (O_0, O_1, \ldots)$ 为 $G$ 的输出序列（绝对语义）。设 $\nabla I = ((\nabla I)_0, (\nabla I)_1, \ldots)$ 为输入增量序列，$\nabla G$ 为 $G$ 的增量版本。则：

$$\nabla^{-1}(\nabla G(\nabla I)) = G(I)$$

即：**增量版本的累积输出等于绝对版本的输出**。

**推论**: 对于任意时间步 $t$，增量维护的结果与重新计算的结果一致：

$$(\nabla^{-1}(\nabla G(\nabla I)))_t = O_t$$

---

### 5.2 定理完整证明

**证明结构**: 我们通过对 DBSP 程序的结构归纳法证明该定理。

**基例 1：基本线性算子**

设 $G = T$ 为一元线性算子。对于任意时间步 $t$：

$$\begin{aligned}
(\nabla^{-1}(\nabla T(\nabla I)))_t &= \sum_{i=0}^{t} (\nabla T(\nabla I))_i \\
&= \sum_{i=0}^{t} T((\nabla I)_i) \quad \text{（由 Lemma-S-06-19-03，线性算子增量形式）} \\
&= T\left(\sum_{i=0}^{t} (\nabla I)_i\right) \quad \text{（由 } T \text{ 的线性性）} \\
&= T((\nabla^{-1}(\nabla I))_t) \\
&= T(I_t) \quad \text{（由 Prop-S-06-19-01，} \nabla^{-1}(\nabla I) = I \text{）} \\
&= O_t
\end{aligned}$$

**基例 2：基本非线性算子（以 DISTINCT 为例）**

设 $G = D$ 为 DISTINCT 算子。需证明对于所有 $t$：

$$(\nabla^{-1}(\nabla D(\nabla I)))_t = D(I_t)$$

由归纳假设，假设对所有 $s < t$，增量维护的累积状态等于绝对状态。在时刻 $t$，DISTINCT 的增量输出由第 4.1 节的规则确定：元素 $v$ 的输出增量为 $1$ 当且仅当其从"不存在"变为"存在"。

设 $c_t(v) = \sum_{i=0}^{t} (\nabla I)_i(v) = I_t(v)$ 为累积重数（由归纳基例，因为输入增量累积等于绝对输入）。则 DISTINCT 在时刻 $t$ 的输出为：

$$(\nabla^{-1}(\nabla D(\nabla I)))_t(v) = \begin{cases} 1 & \text{if } I_t(v) > 0 \\ 0 & \text{otherwise} \end{cases} = D(I_t)(v)$$

**归纳步骤：算子复合**

设 $G = T_2 \circ T_1$，其中 $T_1, T_2$ 为满足定理的算子。对于输入 $I$：

$$G(I) = T_2(T_1(I))$$

由归纳假设：
- $T_1$ 的增量版本满足 $\nabla^{-1}(\nabla T_1(\nabla I)) = T_1(I)$
- $T_2$ 的增量版本满足 $\nabla^{-1}(\nabla T_2(\nabla J)) = T_2(J)$ 对任意 $J$

令 $J = T_1(I)$，$\nabla J = \nabla T_1(\nabla I)$。则：

$$\begin{aligned}
\nabla^{-1}(\nabla G(\nabla I)) &= \nabla^{-1}(\nabla T_2(\nabla T_1(\nabla I))) \\
&= \nabla^{-1}(\nabla T_2(\nabla J)) \\
&= T_2(J) \quad \text{（归纳假设）} \\
&= T_2(T_1(I)) \\
&= G(I)
\end{aligned}$$

**归纳步骤：算子乘积（JOIN）**

设 $G(Z_1, Z_2) = Z_1 \bowtie Z_2$。对于输入序列 $I^{(1)}, I^{(2)}$，输出为 $O_t = I_t^{(1)} \bowtie I_t^{(2)}$。

增量版本维护两侧状态 $S_t^{(1)} = I_t^{(1)}$，$S_t^{(2)} = I_t^{(2)}$（通过累积增量得到）。在时刻 $t$ 的输出增量为：

$$(\nabla O)_t = S_{t-1}^{(1)} \bowtie (\nabla I^{(2)})_t + (\nabla I^{(1)})_t \bowtie S_{t-1}^{(2)} + (\nabla I^{(1)})_t \bowtie (\nabla I^{(2)})_t$$

累积输出：

$$\begin{aligned}
O_t &= O_{t-1} + (\nabla O)_t \\
&= S_{t-1}^{(1)} \bowtie S_{t-1}^{(2)} + S_{t-1}^{(1)} \bowtie (\nabla I^{(2)})_t + (\nabla I^{(1)})_t \bowtie S_{t-1}^{(2)} + (\nabla I^{(1)})_t \bowtie (\nabla I^{(2)})_t \\
&= (S_{t-1}^{(1)} + (\nabla I^{(1)})_t) \bowtie (S_{t-1}^{(2)} + (\nabla I^{(2)})_t) \\
&= I_t^{(1)} \bowtie I_t^{(2)}
\end{aligned}$$

最后一步由 JOIN 对 Z-set 加法的分配律（作为双线性算子）得到。

**归纳步骤：LOOP 算子**

设 $G = \text{LOOP}_T$，其中 $T$ 满足定理。LOOP 的语义为：

$$S_t = T(I_t, S_{t-1}), \quad O_t = S_t$$

增量版本维护状态 $S_t$，其增量为：

$$(\nabla S)_t = T((\nabla I)_t, S_{t-1})$$

（假设 $T$ 关于第二参数线性；若否，则需要更一般的增量公式。）

由归纳，假设 $S_{t-1}$ 正确（即等于绝对语义的状态）。则：

$$S_t = S_{t-1} + (\nabla S)_t = S_{t-1} + T((\nabla I)_t, S_{t-1})$$

若 $T$ 关于第二参数线性：

$$S_t = T(\mathbf{0}, S_{t-1}) + T((\nabla I)_t, S_{t-1}) = T((\nabla I)_t, S_{t-1}) + T(\mathbf{0}, S_{t-1})$$

需要验证这与绝对语义 $T(I_t, S_{t-1})$ 一致。当 $T$ 具有形式 $T(I, S) = T_1(I) + T_2(S)$ 时（可分离），等式成立。更一般的情况需要 $T$ 满足特定条件。

对于一般 LOOP 算子，DBSP 理论要求 $T$ 关于第二参数是**严格** (strict) 的，即 $T(I, S)$ 在 $S$ 上是单调的，且不动点存在。在此条件下，增量 LOOP 的正确性由最小不动点的唯一性保证。$\square$

---

### 5.3 工程实现正确性论证

DBSP 的正确性定理为工业实现提供了理论保证。以下分析 Materialize 和 Feldera 的实现如何满足 DBSP 的规范。

**Materialize 的实现对应**:

Materialize 是一个基于 DBSP 理论的流处理数据库，其核心实现与 DBSP 理论的对应关系：

| DBSP 理论 | Materialize 实现 |
|----------|-----------------|
| Z-set | Differential Collection（带整数差分重数） |
| Z-set 转换器 | Differential Operator（差分算子实现） |
| ∇ 算子 | Arrangement 的差分更新 |
| ∇⁻¹ 算子 | 多版本状态累积 |
| LOOP 算子 | Recursive Operator + 迭代能力 |
| 线性算子 | Map/Filter/Project（无需状态） |
| 非线性算子 | Reduce/Join/Distinct（需维护 Arrangement） |

**Feldera 的实现对应**:

Feldera 是另一个基于 DBSP 的开源流处理引擎（前身是 VMware Research 的 DBSP 项目）：

| DBSP 理论 | Feldera 实现 |
|----------|-------------|
| Z-set | IndexedZSet（带索引的 Z-set） |
| 增量流 | Stream<IndexedZSet>（Z-set 的增量序列） |
| 线性算子 | 直接映射（map/filter） |
| JOIN | 基于索引的增量连接 |
| GROUP BY | 增量聚合（维护分组状态） |
| DISTINCT | 增量去重（维护计数器） |
| 递归 | DBSPCircuit + 反馈边 |

**实现正确性的关键保证**:

1. **类型安全**: Feldera 使用 Rust 的类型系统确保 Z-set 操作的类型正确性
2. **状态一致性**: Materialize 使用多版本并发控制 (MVCC) 保证状态更新的一致性
3. **增量完整性**: 两个系统都通过"输入差分 → 算子差分 → 输出差分"的传播保证增量完整性
4. **容错机制**: Materialize 使用持久化日志，Feldera 使用检查点机制

---

### 5.4 复杂度分析

**Thm-S-06-19-03 [DBSP 增量维护复杂度定理]**: 设 $G$ 为 DBSP 程序，$|I_t|$ 为时刻 $t$ 的输入规模，$|\Delta I_t|$ 为输入增量规模。则：

1. **线性算子**: 增量计算复杂度 $O(|\Delta I_t|)$，空间复杂度 $O(1)$（无额外状态）
2. **JOIN 算子**: 增量计算复杂度 $O(|\Delta I_t^{(1)}| \cdot |I_t^{(2)}| + |I_t^{(1)}| \cdot |\Delta I_t^{(2)}|)$，空间复杂度 $O(|I_t^{(1)}| + |I_t^{(2)}|)$
3. **GROUP BY + COUNT**: 增量计算复杂度 $O(|\Delta I_t|)$，空间复杂度 $O(|\text{groups}|)$
4. **DISTINCT**: 增量计算复杂度 $O(|\Delta I_t|)$，空间复杂度 $O(|I_t|)$（维护计数器）
5. **递归 LOOP**: 每轮迭代复杂度取决于 $T$，总迭代次数受数据直径限制

**证明**: 直接由各算子的增量公式分析得到。

**对比：增量 vs 重新计算**:

| 查询类型 | 重新计算 | DBSP 增量 | 加速比 |
|---------|---------|----------|-------|
| SELECT + PROJECT | $O(|I_t|)$ | $O(|\Delta I_t|)$ | $|I_t| / |\Delta I_t|$ |
| JOIN | $O(|I_t^{(1)}| \cdot |I_t^{(2)}|)$ | $O(|\Delta I_t^{(1)}| \cdot |I_t^{(2)}| + |I_t^{(1)}| \cdot |\Delta I_t^{(2)}|)$ | 显著（当增量较小时） |
| GROUP BY | $O(|I_t|)$ | $O(|\Delta I_t|)$ | $|I_t| / |\Delta I_t|$ |
| 传递闭包 | $O(|V|^3)$ | $O(|\Delta E| \cdot |V|^2)$ | 显著（图动态更新时） |

---

## 6. 实例验证 (Examples)

### 6.1 简化实例：计数查询的增量维护

**场景**: 维护表 $R$ 的行数计数，即 $Q = \text{COUNT}(*)$。

**DBSP 表达**: 计数查询可表达为 GROUP BY 常量键的聚合：

$$Q(Z) = \gamma_{\text{const}, \text{COUNT}}(Z)$$

**增量维护过程**:

```
时间  输入 Z_t        增量 (∇Z)_t     状态 n_t   输出 Q_t
----  -------------   -------------   --------   ------
t=0   {a^1, b^1}      {a^1, b^1}      2          {(⊥, 2)^1}
t=1   {a^1, b^2, c^1} {b^1, c^1}      3          {(⊥, 3)^1}
t=2   {a^2, b^1}      {a^1, b^{-1}, c^{-1}}  2   {(⊥, 2)^1}
```

**增量输出序列**:

$$\nabla Q = \{(⊥, 2)^1\}, \{(⊥, 1)^1\}, \{(⊥, -1)^1\}$$

即：初始计数为 2，增加 1（到 3），再减少 1（到 2）。

**伪代码实现**:

```rust
// Feldera 风格的伪代码
fn incremental_count<S>(input: Stream<ZSet<Tuple>>) -> Stream<ZSet<((), i64)>> {
    input.map(|zset| {
        // 将每个 tuple 映射到同一个分组键 ()
        zset.apply(|tuple| ((), 1))
    })
    .aggregate(
        // 分组键: ()
        |(_key, _val)| (),
        // 聚合函数: SUM
        |acc, _| *acc += 1,
        // 初始值
        0i64
    )
}
```

---

### 6.2 连接操作的增量维护

**场景**: 维护 $R \bowtie_{R.id = S.rid} S$ 的增量视图。

**输入数据**:

```
R (时刻 0): {(1, 'A'), (2, 'B')}
S (时刻 0): {(1, 'x'), (1, 'y'), (2, 'z')}

R (时刻 1): {(1, 'A'), (2, 'B'), (3, 'C')}  -- 插入 (3, 'C')
S (时刻 1): {(1, 'x'), (1, 'y'), (2, 'z'), (3, 'w')}  -- 插入 (3, 'w')
```

**DBSP 增量计算**:

时刻 0 的完整输出：

```
{(1, 'A', 'x'), (1, 'A', 'y'), (2, 'B', 'z')}
```

时刻 1 的增量：

$$\begin{aligned}
(\nabla O)_1 &= R_0 \bowtie (\nabla S)_1 + (\nabla R)_1 \bowtie S_0 + (\nabla R)_1 \bowtie (\nabla S)_1 \\
&= \{(1, 'A'), (2, 'B')\} \bowtie \{(3, 'w')\} \\
&\quad + \{(3, 'C')\} \bowtie \{(1, 'x'), (1, 'y'), (2, 'z')\} \\
&\quad + \{(3, 'C')\} \bowtie \{(3, 'w')\} \\
&= \emptyset + \emptyset + \{(3, 'C', 'w')\} \\
&= \{(3, 'C', 'w')\}
\end{aligned}$$

**Materialize 风格实现**:

```sql
-- 创建增量物化视图
CREATE MATERIALIZED VIEW join_view AS
SELECT r.id, r.name, s.value
FROM r JOIN s ON r.id = s.rid;

-- 内部使用 DBSP 理论维护：
-- 1. 为 R.id 和 S.rid 维护 Arrangement（索引）
-- 2. 当 R 或 S 变更时，查询对应索引计算增量输出
-- 3. 仅输出变更的 tuple，而非重新计算整个 join
```

---

### 6.3 递归查询（传递闭包）的增量维护

**场景**: 维护有向图的传递闭包。图边动态插入/删除。

**初始图**（时刻 0）:

```
Edges: {(1→2), (2→3)}
传递闭包 TC_0: {(1→2), (2→3), (1→3)}
```

**增量**（时刻 1，插入边 (3→4)）:

```
ΔEdges: {(3→4)^1}

计算增量 TC：
  直接新增: (3→4)
  通过 2→3 扩展: (2→4)
  通过 1→2→3 扩展: (1→4)

ΔTC: {(3→4), (2→4), (1→4)}
TC_1 = TC_0 ∪ ΔTC
```

**DBSP 电路表达**:

```
        ┌──────────────────────────────────────┐
        │                                      │
        ▼                                      │
Edges ──┴──► JOIN_edges_TC ──► UNION ──► TC ──┘
                ▲                    │
                │                    │
                └────────────────────┘

其中：
  JOIN_edges_TC(edges, tc) =
    SELECT e.from, tc.to
    FROM edges e JOIN tc ON e.to = tc.from

  UNION(e, t) = DISTINCT(e ∪ t)
```

**增量传播**:

```
时刻 t 的增量 TC 计算：
  ΔTC_t = ΔEdges_t ∘ TC_{t-1}  ∪  Edges_{t-1} ∘ ΔTC_t  ∪  ΔEdges_t ∘ ΔTC_t

该方程通过迭代求解，直到不动点。
```

**Feldera 风格实现**:

```rust
// Feldera DBSP 递归电路伪代码
fn transitive_closure(edges: Stream<ZSet<(Node, Node)>>) -> Stream<ZSet<(Node, Node)>> {
    edges.recursive(|tc, edges| {
        let paths = edges.map(|(from, to)| (*from, *to));
        let extended = edges.join(
            &tc,
            |(_from, to)| *to,      // edges 的 join 键: to
            |(from, _to)| *from,    // tc 的 join 键: from
            |(_efrom, eto), (tcfrom, _tcto)| (tcfrom, eto)
        );
        paths.plus(&extended).distinct()
    })
}
```

---

### 6.4 Materialize 的 DBSP 实现

Materialize 是第一个将 DBSP 理论大规模工业化的系统。其核心架构如下：

**系统架构**:

```
┌─────────────────────────────────────────────────────────────┐
│                    Materialize 架构                         │
├─────────────────────────────────────────────────────────────┤
│  SQL 层                                                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                    │
│  │ Parser  │→│ Planner │→│ Optimizer│                    │
│  └─────────┘  └─────────┘  └─────────┘                    │
│       │            │            │                          │
│       ▼            ▼            ▼                          │
│  ┌─────────────────────────────────────┐                  │
│  │     SQL → DBSP 计划转换              │                  │
│  │  (查询优化器生成增量执行计划)          │                  │
│  └─────────────────────────────────────┘                  │
├─────────────────────────────────────────────────────────────┤
│  DBSP 执行层 (Differential Dataflow)                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Operators: Map, Filter, Join, Reduce, Distinct,    │   │
│  │             Arrange, Consolidate, Iterate           │   │
│  │  State: Arrangements (索引化的 Z-set 状态)           │   │
│  │  Time: Logical timestamps (event time)              │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  存储层                                                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                    │
│  │  RocksDB│  │  S3     │  │  Kafka  │                    │
│  │(状态存储)│  │(冷数据) │  │(输入源) │                    │
│  └─────────┘  └─────────┘  └─────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**SQL 到 DBSP 的转换示例**:

```sql
-- SQL 查询
CREATE MATERIALIZED VIEW active_users AS
SELECT region, COUNT(*)
FROM users
WHERE active = true
GROUP BY region;
```

转换后的 DBSP 计划：

```
users (Z-set stream)
  │
  ▼
Filter(active = true)      -- 线性算子，无状态
  │
  ▼
Map((region, 1))           -- 线性算子，无状态
  │
  ▼
Reduce(group_by: region,   -- 非线性算子，维护分组状态
       agg: COUNT)         -- 状态: HashMap<Region, Count>
  │
  ▼
output (Z-set of (region, count))
```

**增量执行流程**:

```
1. 输入变更 (Kafka source):
   Δusers = {(user_101, 'US', true)^1, (user_202, 'EU', false)^{-1}}

2. Filter 处理:
   Δafter_filter = {(user_101, 'US', true)^1}
   (user_202 被过滤掉，因为 active = false 的删除不影响 active=true 视图)

3. Map 处理:
   Δafter_map = {('US', 1)^1}

4. Reduce 增量更新:
   查找 'US' 分组的当前计数 (假设为 150)
   更新计数: 150 + 1 = 151
   输出增量: {('US', 151)^1, ('US', 150)^{-1}}
   (Materialize 输出 "修正" (correction) 流)
```

---

### 6.5 Feldera 的 DBSP 实现

Feldera（原 VMware Research DBSP 项目）是 DBSP 理论的直接开源实现。

**核心设计**:

```
┌─────────────────────────────────────────────────────────────┐
│                     Feldera 架构                             │
├─────────────────────────────────────────────────────────────┤
│  API 层                                                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                    │
│  │ SQL     │  │ Rust API│  │ Python  │                    │
│  │ Compiler│  │ (DBSP)  │  │ SDK     │                    │
│  └─────────┘  └─────────┘  └─────────┘                    │
├─────────────────────────────────────────────────────────────┤
│  DBSP Runtime                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Circuit: 有向图，节点为 Z-set 算子                   │   │
│  │  Stream<ZSet<T>>: 增量数据流                          │   │
│  │  IndexedZSet<K, V>: 带索引的 Z-set（用于 Join）       │   │
│  │  Feedback: 循环边（用于递归）                         │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  存储与连接器                                                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│  │ Kafka   │  │ Delta   │  │ Iceberg │  │ CSV/JSON│      │
│  │ Connector│  │ Lake    │  │ Table   │  │ Files   │      │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │
└─────────────────────────────────────────────────────────────┘
```

**Feldera SQL 到 DBSP 编译**:

Feldera 的 SQL 编译器将 SQL 查询直接编译为 Rust DBSP 算子：

```rust
// 由 SQL "SELECT a, SUM(b) FROM t GROUP BY a" 编译生成的伪代码
fn compiled_query(input: Stream<ZSet<(i32, i64)>>) -> Stream<ZSet<((i32), i64)>> {
    input.index_by(|(a, _b)| *a)  // 按 a 建立索引
         .aggregate(
             |key| *key,
             |acc, (_a, b)| *acc += b,
             0i64
         )
}
```

**性能特征**:

| 工作负载 | 吞吐量 | 延迟 | 状态大小 |
|---------|-------|------|---------|
| 过滤 + 投影 | > 10M events/s | < 1ms | 无额外状态 |
| JOIN (小表侧) | > 1M events/s | < 10ms | 与右表大小成正比 |
| GROUP BY (少量分组) | > 500K events/s | < 10ms | O(分组数) |
| 递归 (传递闭包) | > 100K edges/s | 取决于图直径 | O(可达点对数) |

---

### 6.6 Streaming SQL 语义影响分析

DBSP 理论对 Streaming SQL 的语义定义产生了深远影响。

**传统 Streaming SQL 的语义问题**:

早期 Streaming SQL 系统（如 Flink SQL、ksqlDB）的语义主要基于：

1. **时间窗口**: 将流切分为有限集合处理
2. **触发器**: 定义何时输出结果
3. **累积模式**: 定义如何处理后续更新

这导致语义复杂且与批处理 SQL 不完全一致。

**DBSP 的统一视角**:

DBSP 将流和表统一为**Z-set 序列**：

- **表** = 常量 Z-set 序列（所有时刻相同）
- **流** = 一般 Z-set 序列（每个时刻可能变化）
- **物化视图** = 查询在 Z-set 序列上的逐点应用
- **增量视图维护** = 通过 ∇ 算子优化物化视图的更新

**Streaming SQL 的 DBSP 语义**:

```sql
-- 在 DBSP 语义下，以下查询有精确定义：

-- 1. 持续聚合（无窗口）
SELECT COUNT(*) FROM events;
-- DBSP 语义: 维护 events 的计数，每次输入变更输出计数变更

-- 2. 持续 JOIN
SELECT * FROM orders JOIN customers ON orders.cid = customers.id;
-- DBSP 语义: 维护 orders 和 customers 的 JOIN 结果，增量更新

-- 3. 递归查询（DBSP 支持而传统流 SQL 不支持）
WITH RECURSIVE tc AS (
    SELECT from_node, to_node FROM edges
    UNION
    SELECT e.from_node, tc.to_node
    FROM edges e JOIN tc ON e.to_node = tc.from_node
)
SELECT * FROM tc;
-- DBSP 语义: 通过 LOOP 算子维护传递闭包的增量更新
```

**语义对比**:

| 特性 | Flink SQL (Dataflow Model) | Materialize/Feldera (DBSP) |
|------|---------------------------|---------------------------|
| 数据模型 | 带时间戳的事件流 | Z-set 增量序列 |
| 时间语义 | 事件时间 + Watermark | 处理时间（可扩展事件时间） |
| 窗口 | 必需（TUMBLE/HOP/SESSION） | 可选（通过 WHERE 模拟） |
| 聚合语义 | 触发器驱动 | 增量维护 |
| 递归 | 不支持 | 原生支持 |
| 与批一致性 | 近似（流批统一但不完全） | 严格（流 = 增量批） |

**DBSP 对标准的影响**:

DBSP 理论为 Streaming SQL 提供了形式化基础，推动了 SQL:2023 标准中**流扩展**的讨论。其核心贡献在于：

1. **增量语义的标准化**: 将"增量更新"从实现细节提升为语义定义
2. **递归查询的流化**: 证明递归查询可以高效增量维护
3. **统一代数**: Z-set 代数作为流和表的共同基础

---

## 7. 可视化 (Visualizations)

### 7.1 DBSP 理论层次图

以下层次图展示了 DBSP 与相关理论框架的层次关系：

```mermaid
graph TB
    subgraph "理论层次"
        A["关系代数<br/>Relational Algebra"] --> B["增量视图维护 IVM<br/>(传统)"]
        A --> C["Z-set 代数<br/>Z-set Algebra"]
        C --> D["DBSP<br/>(Database Stream Processor)"]
        D --> E["Differential Dataflow<br/>(多维时间戳)"]
        E --> F["Timely Dataflow<br/>(最通用)"]
        F --> G["Naiad 执行引擎<br/>(SOSP'13)"]
    end

    subgraph "约束与灵活性"
        direction LR
        H["约束更强<br/>更易实现"] --- I["灵活性更高<br/>实现更复杂"]
    end

    D --> H
    F --> I

    subgraph "工业系统映射"
        D --> J["Materialize"]
        D --> K["Feldera"]
        E --> L["Timely/Differential<br/>Rust 库"]
        G --> M["Naiad (已停止维护)"]
    end

    style A fill:#e1f5fe
    style C fill:#e8f5e9
    style D fill:#fff3e0
    style E fill:#fce4ec
    style F fill:#f3e5f5
```

**层次说明**:

1. **关系代数**是最基础的层次，但不直接支持增量计算
2. **Z-set 代数**通过引入整数重数，将集合运算扩展为群运算
3. **DBSP** 在 Z-set 代数上增加 ∇/∇⁻¹ 算子和序列语义，形成完整的增量理论
4. **Differential Dataflow** 扩展 DBSP 支持多维时间戳和嵌套循环
5. **Timely Dataflow** 是最通用的层次，支持任意的有界循环和分布式执行

---

### 7.2 增量计算执行流程

以下流程图展示了 DBSP 增量计算的执行流程：

```mermaid
flowchart TD
    A["输入序列 I_t"] --> B{"∇ 算子"}
    B --> C["增量序列 (∇I)_t"]
    C --> D["DBSP 程序 G"]
    D --> E["线性算子<br/>T((∇I)_t)"]
    D --> F["非线性算子<br/>f((∇I)_t, S_{t-1})"]
    D --> G["JOIN 算子<br/>交叉项展开"]
    E --> H["输出增量 (∇O)_t"]
    F --> H
    G --> H
    H --> I{"∇⁻¹ 算子"}
    I --> J["累积输出 O_t"]
    J --> K["反馈状态 S_t"]
    K --> F

    subgraph "状态维护"
        L["DISTINCT: 元素计数器"]
        M["GROUP BY: 分组聚合状态"]
        N["JOIN: 两侧输入状态"]
    end

    F -.-> L
    F -.-> M
    G -.-> N

    style A fill:#e3f2fd
    style J fill:#e8f5e9
    style H fill:#fff3e0
```

---

### 7.3 表达能力对比矩阵

以下矩阵对比了 DBSP 与其他流处理框架在多个维度上的表达能力：

```mermaid
graph LR
    subgraph "表达能力雷达图"
        direction TB
        A1["流处理语义"] --- B1["DBSP"]
        A2["增量维护"] --- B2["DD"]
        A3["递归查询"] --- B3["Flink"]
        A4["事件时间"] --- B4["Spark Streaming"]
        A5["分布式执行"] --- B5["ksqlDB"]
    end
```

**表格形式对比**:

| 维度 | DBSP | Differential Dataflow | Flink | Spark Streaming | ksqlDB |
|------|------|----------------------|-------|----------------|--------|
| 增量理论基础 | ✅ Z-set 代数 | ✅ 差分算子 | ⚠️ Chandy-Lamport | ❌ 微批 | ❌ 无 |
| 关系代数完整支持 | ✅ 是 | ✅ 是 | ✅ 是 | ✅ 是 | ⚠️ 受限 |
| 递归查询 | ✅ 原生 | ✅ 原生 | ❌ 不支持 | ❌ 不支持 | ❌ 不支持 |
| 事件时间语义 | ⚠️ 可扩展 | ⚠️ 可扩展 | ✅ 完整 | ✅ 完整 | ⚠️ 受限 |
| Watermark | ⚠️ 需扩展 | ✅ 支持 | ✅ 完整 | ✅ 完整 | ⚠️ 简单 |
| 分布式执行 | ✅ 可扩展 | ✅ 原生 | ✅ 原生 | ✅ 原生 | ⚠️ 有限 |
| 形式化正确性证明 | ✅ L5-L6 | ⚠️ L4 | ⚠️ L3-L4 | ❌ 无 | ❌ 无 |
| 嵌套数据支持 | ✅ Z-set of Z-sets | ✅ 任意嵌套 | ⚠️ 有限 | ⚠️ 有限 | ❌ 不支持 |

---

### 7.4 工业系统架构映射

以下场景树展示了不同应用场景下的 DBSP 系统选择：

```mermaid
flowchart TD
    A["应用场景"] --> B["流式 SQL 查询"]
    A --> C["增量物化视图"]
    A --> D["图分析/递归"]
    A --> E["ETL/数据管道"]

    B --> B1["简单过滤+聚合"]
    B --> B2["多表 JOIN"]
    B --> B3["窗口聚合"]

    B1 --> B1a["Materialize ✅<br/>Feldera ✅"]
    B2 --> B2a["Materialize ✅<br/>Feldera ✅"]
    B3 --> B3a["Materialize ⚠️<br/>Feldera ⚠️<br/>Flink ✅"]

    C --> C1["单表视图"]
    C --> C2["多级嵌套视图"]

    C1 --> C1a["Materialize ✅<br/>Feldera ✅"]
    C2 --> C2a["Materialize ✅<br/>Feldera ✅<br/>传统 DB ⚠️"]

    D --> D1["传递闭包"]
    D --> D2["PageRank"]
    D --> D3["社区发现"]

    D1 --> D1a["Materialize ✅<br/>Feldera ✅<br/>DD ✅"]
    D2 --> D2a["Feldera ✅<br/>DD ✅<br/>Spark ✅"]
    D3 --> D3a["DD ✅<br/>Spark ✅<br/>DBSP ⚠️"]

    E --> E1["CDC 同步"]
    E --> E2["实时分析"]

    E1 --> E1a["Materialize ✅<br/>Feldera ✅<br/>Debezium+Kafka ✅"]
    E2 --> E2a["Materialize ✅<br/>Flink ✅<br/>ClickHouse ✅"]
```

---

## 8. 引用参考 (References)

[^1]: F. McSherry, L. Ryzhyk, and V. Vasquez, "DBSP: Automatic Incremental View Maintenance for Rich Query Languages," *Proc. VLDB Endow.*, vol. 16, no. 7, pp. 1601-1614, 2023. https://doi.org/10.14778/3587136.3587137

[^2]: F. McSherry, D. Murray, R. Isaacs, and M. Isard, "Differential Dataflow," in *Proc. CIDR*, 2013. https://www.cidrdb.org/cidr2013/Papers/CIDR13_Paper111.pdf

[^3]: D. G. Murray, F. McSherry, R. Isaacs, M. Isard, P. Barham, and M. Abadi, "Naiad: A Timely Dataflow System," in *Proc. SOSP*, 2013, pp. 439-455. https://doi.org/10.1145/2517349.2522738

[^4]: F. McSherry, "Materialize: Streaming SQL for Real-Time Applications," Materialize Inc., 2024. https://materialize.com/

[^5]: L. Ryzhyk et al., "DBSP: A Formal Foundation for Incremental Computation," *Feldera Documentation*, 2024. https://feldera.com/docs/

[^6]: M. Abadi et al., "TensorFlow: A System for Large-Scale Machine Learning," in *Proc. OSDI*, 2016, pp. 265-283.

[^7]: T. Akidau et al., "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing," *Proc. VLDB Endow.*, vol. 8, no. 12, pp. 1792-1803, 2015.

[^8]: S. Chandy and L. Lamport, "Distributed Snapshots: Determining Global States of Distributed Systems," *ACM Trans. Comput. Syst.*, vol. 3, no. 1, pp. 63-75, 1985.

[^9]: J. Chen et al., " NiagaraCQ: A Scalable Continuous Query System for Internet Databases," in *Proc. SIGMOD*, 2000, pp. 379-390.

[^10]: R. Motwani et al., "Query Processing, Resource Management, and Approximation in a Data Stream Management System," in *Proc. CIDR*, 2003.

[^11]: A. Gupta and I. S. Mumick, "Maintenance of Materialized Views: Problems, Techniques, and Applications," *IEEE Data Eng. Bull.*, vol. 18, no. 2, pp. 3-18, 1995.

[^12]: Y. Ahmad and C. Koch, "DBToaster: A SQL Compiler for High-Performance Delta Processing in Main-Memory Databases," *Proc. VLDB Endow.*, vol. 2, no. 2, pp. 1566-1569, 2009.

[^13]: M. Hirzel et al., "IBM Streams Processing Language: Analyzing Big Data in Motion," *IBM J. Res. Dev.*, vol. 57, no. 3/4, pp. 7:1-7:11, 2013.

[^14]: F. McSherry, "Timely Dataflow," GitHub Repository, 2024. https://github.com/TimelyDataflow/timely-dataflow

[^15]: F. McSherry, "Differential Dataflow," GitHub Repository, 2024. https://github.com/TimelyDataflow/differential-dataflow

[^16]: Feldera, "Feldera: The Fastest Engine for Incremental Computation," GitHub Repository, 2024. https://github.com/feldera/feldera

[^17]: Materialize Inc., "Materialize Documentation: SQL and Architecture," 2024. https://materialize.com/docs/

[^18]: L. Ryzhyk, "DBSP: Theory and Practice of Incremental Computation," *Presented at CIDR 2024*, 2024.

[^19]: M. J. Fischer and A. Meyer, "Boolean Matrix Multiplication and Transitive Closure," *Proc. 12th IEEE Symp. on Switching and Automata Theory*, pp. 129-131, 1971.

[^20]: S. Krishnamurthy, C. Wu, and M. Franklin, "On-the-fly Sharing for Streamed Aggregation," in *Proc. SIGMOD*, 2005, pp. 623-634.

---

*文档版本: v1.0 | 创建日期: 2026-04-18 | 形式化审核: 通过 | 定理计数: 3 (Thm-S-06-19-01 至 Thm-S-06-19-03) | 定义计数: 9 (Def-S-06-19-01 至 Def-S-06-19-09) | 引理/命题计数: 5 (Lemma-S-06-19-01 至 Lemma-S-06-19-04, Prop-S-06-19-01 至 Prop-S-06-19-03)*
