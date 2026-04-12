# First-Person Choreographic Programming (1CP) 前沿深度解析

> **所属阶段**: Struct/06-frontier/first-person-choreographies | **前置依赖**: [06.02-choreographic-streaming-programming.md](../06.02-choreographic-streaming-programming.md) | **形式化等级**: L6
> **文档状态**: v1.0 | **创建日期**: 2026-04-13

---

## 核心摘要

First-Person Choreographic Programming (1CP) 是Choreographic Programming范式的最新演进，由Graversen等人在2025年提出。与传统第三人称Choreography（从全局视角描述）不同，1CP从参与者自身视角（第一人称）描述分布式交互，支持运行时动态角色发现和进程参数化。

## 1. 概念定义 (Definitions)

### Def-S-06-1CP-01: 第一人称Choreography形式化

$$
\mathcal{C}_{1CP} ::= (\mathcal{R}, \mathcal{M}, \Sigma, \Pi_{dyn}, \rightsquigarrow)
$$

其中 $\Pi_{dyn}$ 为动态端点投影运算符，在运行时（而非编译时）将全局Choreography分解为本地行为。

### Def-S-06-1CP-02: 延续传递通信 (CPC)

$$
\text{CPC} ::= send(receiver, value, \lambda state. continuation)
$$

### Def-S-06-1CP-03: Census Polymorphism

允许Choreography抽象于参与者数量：

$$
\Lambda n. \Lambda \vec{\rho}:\{Role\}^n. \mathcal{C}(\vec{\rho})
$$

## 2. 关键定理

### Thm-S-06-1CP-01: 动态EPP正确性

动态EPP生成的本地程序，其组合行为与全局Choreography一致。

### Thm-S-06-1CP-02: 1CP完整性

1CP可表达所有静态Choreography可表达的协议，以及部分动态协议。

## 3. 与流处理的融合

1CP特别适用于动态流处理拓扑：

- 运行时动态增减TaskManager
- 自适应分区策略
- 弹性扩缩容协议

## 4. 引用
