# Struct/ 形式化理论文档索引

> **版本**: 2026.04 | **范围**: 统一流计算理论形式化体系 | **文档总数**: 28 核心文档 (18 基础层 + 10 扩展层)

---

## 目录

- [Struct/ 形式化理论文档索引](#struct-形式化理论文档索引)
  - [目录](#目录)
  - [1. 快速导航](#1-快速导航)
  - [2. 文档架构概览](#2-文档架构概览)
  - [3. 定理注册表 (Theorem Registry)](#3-定理注册表-theorem-registry)
    - [3.2 前沿研究层定理 (06-frontier)](#32-前沿研究层定理-06-frontier)
    - [3.3 形式化工具层定理 (07-tools)](#33-形式化工具层定理-07-tools)
    - [3.4 标准规范层定理 (08-standards)](#34-标准规范层定理-08-standards)
  - [4. 定义注册表 (Definition Registry)](#4-定义注册表-definition-registry)
    - [4.1 基础层定义 (01-foundation)](#41-基础层定义-01-foundation)
    - [4.2 性质层定义 (02-properties)](#42-性质层定义-02-properties)
    - [4.3 关系层定义 (03-relationships)](#43-关系层定义-03-relationships)
    - [4.4 证明层定义 (04-proofs)](#44-证明层定义-04-proofs)
    - [4.5 前沿层定义 (06-frontier)](#45-前沿层定义-06-frontier)
    - [4.6 工具层定义 (07-tools)](#46-工具层定义-07-tools)
    - [4.7 标准层定义 (08-standards)](#47-标准层定义-08-standards)
  - [5. 引理注册表 (Lemma Registry)](#5-引理注册表-lemma-registry)
    - [5.2 前沿层引理 (06-frontier)](#52-前沿层引理-06-frontier)
    - [5.3 工具层引理 (07-tools)](#53-工具层引理-07-tools)
    - [5.4 标准层引理 (08-standards)](#54-标准层引理-08-standards)
  - [6. 性质与推论注册表](#6-性质与推论注册表)
    - [6.2 前沿层性质与推论 (06-frontier)](#62-前沿层性质与推论-06-frontier)
    - [6.3 工具层性质与推论 (07-tools)](#63-工具层性质与推论-07-tools)
    - [6.4 标准层性质与推论 (08-standards)](#64-标准层性质与推论-08-standards)
  - [7. 核心概念速查表](#7-核心概念速查表)
    - [7.1 六层表达能力层次 (L1-L6)](#71-六层表达能力层次-l1-l6)
    - [7.2 一致性层级](#72-一致性层级)
    - [7.3 模型编码关系](#73-模型编码关系)
  - [8. 文档依赖图](#8-文档依赖图)
    - [8.1 层级依赖关系](#81-层级依赖关系)
    - [8.2 跨层依赖关系](#82-跨层依赖关系)
  - [9. 推荐阅读路径](#9-推荐阅读路径)
    - [9.1 研究者路径 (Researcher)](#91-研究者路径-researcher)
    - [9.2 工程师路径 (Engineer)](#92-工程师路径-engineer)
    - [9.3 学生路径 (Student)](#93-学生路径-student)
    - [9.4 前沿探索路径 (Frontier Explorer)](#94-前沿探索路径-frontier-explorer)
  - [10. 关键结果汇总](#10-关键结果汇总)
    - [10.1 核心理论结果](#101-核心理论结果)
    - [10.2 工程指导原则](#102-工程指导原则)
    - [10.3 开放问题](#103-开放问题)
    - [10.4 前沿研究进展 (06-frontier)](#104-前沿研究进展-06-frontier)
  - [11. 文档清单](#11-文档清单)
    - [11.1 完整文档列表](#111-完整文档列表)
    - [11.2 文档统计](#112-文档统计)
    - [11.3 新增前沿与工具文档 (06-08)](#113-新增前沿与工具文档-06-08)
    - [11.4 更新后完整统计](#114-更新后完整统计)

---

## 1. 快速导航

| 类别 | 快速链接 |
|------|----------|
| **基础理论** | [01.01 USTM统一理论](./01-foundation/01.01-unified-streaming-theory.md) · [01.02 进程演算](./01-foundation/01.02-process-calculus-primer.md) |
| **模型形式化** | [01.03 Actor模型](./01-foundation/01.03-actor-model-formalization.md) · [01.04 Dataflow](./01-foundation/01.04-dataflow-model-formalization.md) · [01.05 CSP](./01-foundation/01.05-csp-formalization.md) · [01.06 Petri网](./01-foundation/01.06-petri-net-formalization.md) |
| **核心性质** | [02.01 确定性](./02-properties/02.01-determinism-in-streaming.md) · [02.02 一致性层次](./02-properties/02.02-consistency-hierarchy.md) · [02.03 Watermark单调性](./02-properties/02.03-watermark-monotonicity.md) · [02.04 活性/安全性](./02-properties/02.04-liveness-and-safety.md) · [02.05 类型安全](./02-properties/02.05-type-safety-derivation.md) |
| **模型关系** | [03.01 Actor→CSP编码](./03-relationships/03.01-actor-to-csp-encoding.md) · [03.02 Flink→进程演算](./03-relationships/03.02-flink-to-process-calculus.md) · [03.03 表达能力层次](./03-relationships/03.03-expressiveness-hierarchy.md) |
| **形式证明** | [04.01 Checkpoint正确性](./04-proofs/04.01-flink-checkpoint-correctness.md) · [04.02 Exactly-Once正确性](./04-proofs/04.02-flink-exactly-once-correctness.md) · [04.03 Chandy-Lamport一致性](./04-proofs/04.03-chandy-lamport-consistency.md) |
| **比较分析** | [05.01 Go vs Scala](./05-comparative-analysis/05.01-go-vs-scala-expressiveness.md) |
| **前沿研究** | [06.01 开放问题](./06-frontier/06.01-open-problems-streaming-verification.md) · [06.02 Choreographic流编程](./06-frontier/06.02-choreographic-streaming-programming.md) · [06.03 AI Agent与会话类型](./06-frontier/06.03-ai-agent-session-types.md) · [06.04 pDOT路径依赖类型](./06-frontier/06.04-pdot-path-dependent-types.md) |
| **形式化工具** | [Coq机械化证明](./07-tools/coq-mechanization.md) · [TLA+验证Flink](./07-tools/tla-for-flink.md) · [Iris分离逻辑](./07-tools/iris-separation-logic.md) · [模型检查实践](./07-tools/model-checking-practice.md) · [Smart Casual验证](./07-tools/smart-casual-verification.md) |
| **标准规范** | [流式SQL标准](./08-standards/streaming-sql-standard.md) |

---

## 2. 文档架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                        01-foundation                              │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐        │
│  │  01.01   │  01.02   │  01.03   │  01.04   │  01.05   │  01.06 │
│  │   USTM   │ 进程演算 │  Actor   │ Dataflow │   CSP    │ Petri网│
│  └──────────┴──────────┴──────────┴──────────┴──────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        02-properties                              │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐        │
│  │  02.01   │  02.02   │  02.03   │  02.04   │  02.05   │        │
│  │ 确定性   │ 一致性   │ Watermark│ 活性/安全│ 类型安全 │        │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      03-relationships                             │
│  ┌──────────────────┬──────────────────┬──────────────────┐      │
│  │      03.01       │      03.02       │      03.03       │      │
│  │  Actor→CSP编码   │ Flink→进程演算   │ 表达能力层次     │      │
│  └──────────────────┴──────────────────┴──────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        04-proofs                                  │
│  ┌──────────────────┬──────────────────┬──────────────────┐      │
│  │      04.01       │      04.02       │      04.03       │      │
│  │ Checkpoint正确性 │ Exactly-Once     │ Chandy-Lamport   │      │
│  └──────────────────┴──────────────────┴──────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    05-comparative-analysis                        │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                        05.01                             │    │
│  │                   Go vs Scala                            │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      06-frontier (前沿研究)                        │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐   │
│  │    06.01     │    06.02     │    06.03     │    06.04     │   │
│  │   开放问题   │ Choreographic│  AI Agent    │    pDOT      │   │
│  │              │   流编程     │  会话类型    │  路径依赖类型│   │
│  └──────────────┴──────────────┴──────────────┴──────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │              first-person-choreographies                 │    │
│  │                   第一人称Choreographic                   │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        07-tools (形式化工具)                       │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐   │
│  │    Coq       │    TLA+      │    Iris      │    模型检查   │   │
│  │  机械化证明   │  验证Flink   │  分离逻辑    │    实践      │   │
│  └──────────────┴──────────────┴──────────────┴──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      08-standards (标准规范)                       │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                   streaming-sql-standard                 │    │
│  │                      流式SQL标准                          │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

**层级说明**:

- **01-foundation**: 建立USTM元模型和五大计算模型（Actor, CSP, Dataflow, Petri, 进程演算）的形式化基础
- **02-properties**: 证明流计算核心性质（确定性、一致性、Watermark单调性、活性/安全性、类型安全）
- **03-relationships**: 建立模型间的编码关系，定义六层表达能力层次（L1-L6）
- **04-proofs**: Flink Checkpoint和Exactly-Once语义的形式化正确性证明
- **05-comparative**: 编程语言表达能力的对比分析（Go vs Scala）
- **06-frontier**: 前沿研究方向，包括Choreographic编程、AI Agent会话类型、路径依赖类型等
- **07-tools**: 形式化验证工具实践，包括Coq、TLA+、Iris分离逻辑、模型检查等
- **08-standards**: 流计算相关标准规范，包括SQL:2011/2023流扩展标准

---

## 3. 定理注册表 (Theorem Registry)

| 定理编号 | 名称 | 位置 | 形式化等级 | 依赖 |
|----------|------|------|------------|------|
| **Thm-S-01-01** | USTM组合性定理 | 01-foundation/01.01 | L4 | Def-S-01-01 |
| **Thm-S-01-02** | 表达能力层次可判定性 | 01-foundation/01.01 | L4 | Def-S-01-02 |
| **Thm-S-02-01** | π-演算严格包含CSP/CCS | 01-foundation/01.02 | L4 | Def-S-02-03 |
| **Thm-S-03-01** | Actor局部确定性定理 | 01-foundation/01.03 | L4 | Def-S-03-01, Lemma-S-03-01 |
| **Thm-S-03-02** | 监督树活性定理 | 01-foundation/01.03 | L4 | Def-S-03-05 |
| **Thm-S-04-01** | Dataflow确定性定理 | 01-foundation/01.04 | L4 | Def-S-04-01, Def-S-04-04 |
| **Thm-S-05-01** | Go-CS-sync ↔ CSP迹等价 | 01-foundation/01.05 | L3 | Def-S-05-01, Def-S-05-05 |
| **Thm-S-06-01** | Petri网活性有界性刻画 | 01-foundation/01.06 | L2 | Def-S-06-01 |
| **Thm-S-07-01** | 流计算确定性定理 | 02-properties/02.01 | L4 | Def-S-07-01, Lemma-S-07-02 |
| **Thm-S-08-01** | Exactly-Once必要条件 | 02-properties/02.02 | L5 | Def-S-08-04 |
| **Thm-S-08-02** | 端到端Exactly-Once正确性 | 02-properties/02.02 | L5 | Prop-S-08-01 |
| **Thm-S-08-03** | 统一一致性格 | 02-properties/02.02 | L4 | Def-S-08-01 |
| **Thm-S-09-01** | Watermark单调性定理 | 02-properties/02.03 | L4 | Def-S-09-02, Lemma-S-04-02 |
| **Thm-S-10-01** | Actor安全/活性组合性 | 02-properties/02.04 | L4 | Def-S-10-01, Def-S-10-02 |
| **Thm-S-11-01** | 类型安全（Progress + Preservation） | 02-properties/02.05 | L3 | Def-S-11-02 |
| **Thm-S-12-01** | 受限Actor系统编码保持迹语义 | 03-relationships/03.01 | L4 | Def-S-12-03, Lemma-S-12-01 |
| **Thm-S-13-01** | Flink Dataflow Exactly-Once保持 | 03-relationships/03.02 | L5 | Def-S-13-03, Lemma-S-13-02 |
| **Thm-S-14-01** | 表达能力严格层次定理 | 03-relationships/03.03 | L3-L6 | Def-S-14-01, Def-S-14-03 |
| **Thm-S-17-01** | Flink Checkpoint一致性定理 | 04-proofs/04.01 | L5 | Def-S-17-02, Lemma-S-17-02 |
| **Thm-S-18-01** | Flink Exactly-Once正确性定理 | 04-proofs/04.02 | L5 | Lemma-S-18-01, Lemma-S-18-02 |
| **Thm-S-18-02** | 幂等Sink等价性定理 | 04-proofs/04.02 | L5 | Def-S-18-05 |
| **Thm-S-19-01** | Chandy-Lamport一致性定理 | 04-proofs/04.03 | L5 | Def-S-19-02, Lemma-S-19-02 |
| **Thm-S-24-01** | Go与Scala图灵完备等价 | 05-comparative/05.01 | L6 | FG, DOT |

### 3.2 前沿研究层定理 (06-frontier)

| 定理编号 | 名称 | 位置 | 形式化等级 | 依赖 |
|----------|------|------|------------|------|
| **Thm-S-20-01** | Choreographic流程序正确性 | 06-frontier/06.02 | L5 | Def-S-20-01~06 |
| **Thm-S-20-02** | 全局类型推断完备性 | 06-frontier/06.02 | L5 | Def-S-20-06 |
| **Thm-S-06-01** | 1CP死锁自由保证 | 06-frontier/first-person-choreographies | L5 | Def-S-06-10~12 |
| **Thm-S-06-02** | 投影算法完备性 (1CP) | 06-frontier/first-person-choreographies | L5 | Lemma-S-06-01 |
| **Thm-S-06-03** | 1CP与Census互编码 | 06-frontier/first-person-choreographies | L5 | Thm-S-06-02 |
| **Thm-S-06-01** | pDOT类型安全性 | 06-frontier/06.04 | L5-L6 | Def-S-06-07~10 |
| **Thm-S-29-01** | AI Agent系统死锁自由定理 | 06-frontier/06.03 | L5 | Def-S-29-01~06 |

### 3.3 形式化工具层定理 (07-tools)

| 定理编号 | 名称 | 位置 | 形式化等级 | 依赖 |
|----------|------|------|------------|------|
| **Thm-S-07-01** | Watermark单调性Coq形式化 | 07-tools/coq-mechanization | L5 | Def-S-07-07~10 |
| **Thm-S-07-02** | Checkpoint一致性形式化 | 07-tools/coq-mechanization | L5 | Def-S-07-08 |
| **Thm-S-07-01** | Checkpoint协议TLA+不变式 | 07-tools/tla-for-flink | L5 | Def-S-07-01~02 |
| **Thm-S-07-01** | Iris健全性 (Soundness) | 07-tools/iris-separation-logic | L6 | Def-S-07-03~06 |
| **Thm-S-07-02** | 高阶幽灵状态完备性 | 07-tools/iris-separation-logic | L6 | Def-S-07-05 |

### 3.4 标准规范层定理 (08-standards)

| 定理编号 | 名称 | 位置 | 形式化等级 | 依赖 |
|----------|------|------|------------|------|
| **Thm-S-08-01** | SQL:2011窗口函数流正确性 | 08-standards/streaming-sql-standard | L4 | Def-S-08-01~03 |

---

## 4. 定义注册表 (Definition Registry)

### 4.1 基础层定义 (01-foundation)

| 定义编号 | 名称 | 位置 | 说明 |
|----------|------|------|------|
| **Def-S-01-01** | USTM六元组 | 01.01 | 统一流计算理论元模型: <P, C, S, T, Σ, M> |
| **Def-S-01-02** | 六层表达能力层次 (L1-L6) | 01.01 | L1(Regular) → L6(Turing-complete) |
| **Def-S-01-07** | UCM统一并发模型 | 01.01 | 抽象 Actor/CSP/Dataflow/Petri 的并集 |
| **Def-S-02-01** | CCS语法与SOS语义 | 01.02 | 进程代数基础 |
| **Def-S-02-02** | CSP语法 | 01.02 | STOP/SKIP, □/⊓选择, \\|/\\|/\\|并行 |
| **Def-S-02-03** | π-演算 | 01.02 | 带移动性的进程演算 (νa, 名传递) |
| **Def-S-03-01** | 经典Actor四元组 | 01.03 | <α, b, m, σ>: 地址, 行为, 邮箱, 状态 |
| **Def-S-03-05** | 监督树结构 | 01.03 | one_for_one, one_for_all, rest_for_one |
| **Def-S-04-01** | Dataflow图 (DAG) | 01.04 | <V, E, P, Σ, 𝕋>: 顶点, 边, 并行度, 状态, 时间 |
| **Def-S-04-04** | Watermark语义 | 01.04 | 进度指示器: ω(t) ≤ t |
| **Def-S-04-05** | 窗口算子 | 01.04 | Tumbling/Sliding/Session |
| **Def-S-05-01** | CSP核心语法 | 01.05 | STOP/SKIP, □/⊓, \\|/\\|/\\|/\\| |
| **Def-S-05-03** | 迹/失败/发散语义 | 01.05 | 三种语义域 |
| **Def-S-05-05** | Go到CSP编码函数 | 01.05 | [[·]]: Go → CSP |
| **Def-S-06-01** | P/T网六元组 | 01.06 | <P, T, F, W, M₀>: 库所, 变迁, 流, 权重, 初始标识 |
| **Def-S-06-04** | 着色Petri网 (CPN) | 01.06 | 带数据抽象的Petri网 |

### 4.2 性质层定义 (02-properties)

| 定义编号 | 名称 | 位置 | 说明 |
|----------|------|------|------|
| **Def-S-07-01** | 确定性流计算系统 | 02.01 | 六元组: <V, E, F, Σ, 𝕋, P> |
| **Def-S-07-02** | 合流规约语义 | 02.01 | Confluent reduction |
| **Def-S-08-01** | At-Most-Once语义 | 02.02 | 效果计数 ≤ 1 |
| **Def-S-08-02** | At-Least-Once语义 | 02.02 | 效果计数 ≥ 1 |
| **Def-S-08-03** | 幂等性 | 02.02 | f(f(x)) = f(x) |
| **Def-S-08-04** | Exactly-Once语义 | 02.02 | 因果影响计数 = 1 |
| **Def-S-09-02** | Watermark进度语义 | 02.03 | 单调不减的进度指示器 |
| **Def-S-10-01** | 安全性 (Safety) | 02.04 | 闭集: 有限可证 |
| **Def-S-10-02** | 活性 (Liveness) | 02.04 | 稠密集: 无限承诺 |
| **Def-S-11-02** | Featherweight Go语法 | 02.05 | FG: 结构子类型演算 |
| **Def-S-11-03** | Generic Go语法 | 02.05 | FGG: 带约束泛型 |
| **Def-S-11-04** | DOT路径依赖类型 | 02.05 | 依赖对象类型演算 |

### 4.3 关系层定义 (03-relationships)

| 定义编号 | 名称 | 位置 | 说明 |
|----------|------|------|------|
| **Def-S-12-01** | Actor配置四元组 | 03.01 | γ ≜ <A, M, Σ, addr> |
| **Def-S-12-02** | CSP核心语法子集 | 03.01 | 编码目标语言子集 |
| **Def-S-12-03** | Actor→CSP编码函数 | 03.01 | [[·]]_{A→C} |
| **Def-S-12-04** | 受限Actor系统 | 03.01 | 无动态地址传递 |
| **Def-S-13-01** | Flink算子→π-演算编码 | 03.02 | ℰ_op: Operator → π-Process |
| **Def-S-13-02** | Dataflow边→π-演算通道 | 03.02 | ℰ_edge: E → ChannelSet |
| **Def-S-13-03** | Checkpoint→屏障同步协议 | 03.02 | ℰ_chkpt: Checkpoint → BarrierProtocol |
| **Def-S-13-04** | 状态算子→带状态进程 | 03.02 | ℰ_state: StatefulOperator → π-Process |
| **Def-S-14-01** | 表达能力预序 | 03.03 | ⊆: 编码存在性 |
| **Def-S-14-02** | 互模拟等价 | 03.03 | ~ 和 ≈ |
| **Def-S-14-03** | 六层表达能力层次 | 03.03 | ℒ = {L₁, L₂, L₃, L₄, L₅, L₆} |

### 4.4 证明层定义 (04-proofs)

| 定义编号 | 名称 | 位置 | 说明 |
|----------|------|------|------|
| **Def-S-17-01** | Checkpoint Barrier语义 | 04.01 | B_n = <BARRIER, cid, ts, source> |
| **Def-S-17-02** | 一致全局状态 | 04.01 | G = <𝒮, 𝒞> |
| **Def-S-17-03** | Checkpoint对齐 | 04.01 | 多输入算子Barrier同步 |
| **Def-S-17-04** | 状态快照原子性 | 04.01 | 同步阶段 + 异步阶段 |
| **Def-S-18-01** | Exactly-Once语义 | 04.02 | |{e \| caused_by(e,r)}| = 1 |
| **Def-S-18-02** | 端到端一致性 | 04.02 | Replayable ∧ ConsistentCheckpoint ∧ AtomicOutput |
| **Def-S-18-03** | 两阶段提交协议 (2PC) | 04.02 | Prepare + Commit/Abort |
| **Def-S-18-04** | 可重放Source | 04.02 | Read(Src, o) = f(o) |
| **Def-S-18-05** | 幂等性 | 04.02 | f(f(x)) = f(x) |
| **Def-S-19-01** | 全局状态 | 04.03 | S_global = <LS₁, ..., LS_n, {Q_c}> |
| **Def-S-19-02** | 一致割集 | 04.03 | happens-before封闭性 |
| **Def-S-19-03** | 通道状态 | 04.03 | Q*_ij: Marker前后消息集合 |
| **Def-S-19-04** | Marker消息 | 04.03 | <MARKER, snapshotID, source> |
| **Def-S-19-05** | 本地快照 | 04.03 | ℒ_i = <LS*_i, {Q*_ji}> |

### 4.5 前沿层定义 (06-frontier)

| 定义编号 | 名称 | 位置 | 说明 |
|----------|------|------|------|
| **Def-S-20-01** | Choreographic Programming核心概念 | 06.02 | 四元组 (𝒭, ℐ, 𝒞, 𝒫) |
| **Def-S-20-02** | Choreographic流程序 | 06.02 | (𝒪, ℰ, 𝒯, 𝒢) |
| **Def-S-20-03** | 多参与方会话类型 MPST | 06.02 | 带流处理特化的全局类型 |
| **Def-S-20-04** | 全局类型投影 | 06.02 | π(G, p) = G|_p |
| **Def-S-20-05** | Choreographic Dataflow图 | 06.02 | (V, E, λ, G) |
| **Def-S-20-06** | 全局类型推断系统 | 06.02 | 从程序推断全局协议 |
| **Def-S-25-01** | 验证问题谱系 | 06.01 | 𝒱𝒮𝒫 = (𝒫, ℒ, ℱ, ℳ) |
| **Def-S-25-02** | 可判定性边界 | 06.01 | L1-L6可判定性层次 |
| **Def-S-25-03** | 实用验证挑战 | 06.01 | (S, φ, ℛ, 𝒯, 𝒞) |
| **Def-S-25-04** | 开放问题分类 | 06.01 | 理论/工程/混合问题树 |
| **Def-S-29-01** | AI Agent形式化模型 | 06.03 | (S, L, M, π, δ, λ) |
| **Def-S-29-02** | Multi-Agent会话类型 MAST | 06.03 | 带认知条件的会话类型 |
| **Def-S-29-03** | LLM-Agent交互协议 | 06.03 | ReAct模式的类型表达 |
| **Def-S-29-04** | 类型安全Agent通信 | 06.03 | 四元组安全条件 |
| **Def-S-29-05** | Agent协议验证框架 | 06.03 | 静态/运行时/事后三层 |
| **Def-S-29-06** | 认知会话类型 | 06.03 | K_p φ 认知模态 |
| **Def-S-06-07** | pDOT Calculus | 06.04 | 路径依赖类型演算 |
| **Def-S-06-08** | 路径依赖类型 | 06.04 | 任意长度路径 p.a.b.T |
| **Def-S-06-09** | Singleton类型 | 06.04 | p.type 精确类型追踪 |
| **Def-S-06-10** | 精确对象类型 | 06.04 | this.type链式传递 |
| **Def-S-06-10** | 第一人称Choreographic编程 1CP | first-person-choreographies | 五元组 (𝒫, 𝒞, 𝒯, ℳ, 𝒮) |
| **Def-S-06-11** | 进程参数化 | first-person-choreographies | Λ𝑝⃗.C 高阶进程抽象 |
| **Def-S-06-12** | Continuation-Passing通信 | first-person-choreographies | 带延续的通信范式 |

### 4.6 工具层定义 (07-tools)

| 定义编号 | 名称 | 位置 | 说明 |
|----------|------|------|------|
| **Def-S-07-01** | TLA+规格语言 | 07-tools/tla-for-flink | 时序逻辑+集合论 |
| **Def-S-07-02** | 状态机精化 | 07-tools/tla-for-flink | S_low ⊑ S_high |
| **Def-S-07-03** | 分离逻辑断言 | 07-tools/iris-separation-logic | emp, *, ↦ |
| **Def-S-07-04** | 高阶幽灵状态 | 07-tools/iris-separation-logic | HORA资源代数 |
| **Def-S-07-05** | 资源代数 RA | 07-tools/iris-separation-logic | (M, ·, ε, \|·\|, 𝒱) |
| **Def-S-07-06** | 不变式与原子性 | 07-tools/iris-separation-logic | Inv, ⟨a⟩, ⊣⊢ |
| **Def-S-07-07** | Coq归纳类型 | 07-tools/coq-mechanization | Inductive定义 |
| **Def-S-07-08** | 依赖类型与规约 | 07-tools/coq-mechanization | Π(x:A).B(x) |
| **Def-S-07-09** | 策略证明 | 07-tools/coq-mechanization | tac: (Γ⊢τ)→List[(Γ'⊢τ')] |
| **Def-S-07-10** | 共归纳类型 | 07-tools/coq-mechanization | CoInductive Stream |
| **Def-S-07-10** | 模型检查 | 07-tools/model-checking-practice | (S, S₀, R, L) |
| **Def-S-07-11** | LTL/CTL时序逻辑 | 07-tools/model-checking-practice | ○, 𝒰, □, ◇ |
| **Def-S-07-12** | 状态爆炸问题 | 07-tools/model-checking-practice | kⁿ 指数增长 |

### 4.7 标准层定义 (08-standards)

| 定义编号 | 名称 | 位置 | 说明 |
|----------|------|------|------|
| **Def-S-08-01** | SQL:2011流扩展 | 08-standards/streaming-sql-standard | 窗口函数+时间周期 |
| **Def-S-08-02** | 窗口函数标准语法 | 08-standards/streaming-sql-standard | OVER/PARTITION/ORDER |
| **Def-S-08-03** | 流表对偶性 | 08-standards/streaming-sql-standard | Stream↔Table转换 |

---

## 5. 引理注册表 (Lemma Registry)

| 引理编号 | 名称 | 位置 | 关键作用 |
|----------|------|------|----------|
| **Lemma-S-03-01** | Actor邮箱串行处理引理 | 01.03 | 保证局部确定性 |
| **Lemma-S-04-02** | Watermark单调性引理 | 01.04 | Thm-S-09-01前提 |
| **Lemma-S-05-01** | 外部选择就绪集保持 | 01.05 | CSP语义保持 |
| **Lemma-S-06-01** | Karp-Miller树有限性 | 01.06 | 覆盖性可判定 |
| **Lemma-S-07-02** | Watermark单调性蕴含触发确定性 | 02.01 | Thm-S-07-01支撑 |
| **Lemma-S-10-01** | 安全性有限见证 | 02.04 | Alpern-Schneider分解 |
| **Lemma-S-10-02** | 活性无限承诺 | 02.04 | Alpern-Schneider分解 |
| **Lemma-S-11-01** | 替换引理 | 02.05 | 类型安全证明 |
| **Lemma-S-12-01** | MAILBOX FIFO不变式 | 03.01 | Thm-S-12-01核心 |
| **Lemma-S-12-02** | Actor进程单线程性 | 03.01 | 状态隔离证明 |
| **Lemma-S-12-03** | 状态不可外部访问 | 03.01 | 状态封装证明 |
| **Lemma-S-13-01** | 算子编码保持局部确定性 | 03.02 | Thm-S-13-01支撑 |
| **Lemma-S-13-02** | 屏障对齐保证快照一致性 | 03.02 | Thm-S-13-01核心 |
| **Lemma-S-14-01** | 组合性编码状态空间上界 | 03.03 | 编码判据 |
| **Lemma-S-14-02** | 动态拓扑不可回归性 | 03.03 | L₃ ⊂ L₄证明 |
| **Lemma-S-17-01** | Barrier传播不变式 | 04.01 | Thm-S-17-01 Part 1 |
| **Lemma-S-17-02** | 状态一致性引理 | 04.01 | Thm-S-17-01 Part 2 |
| **Lemma-S-17-03** | 对齐点唯一性 | 04.01 | 快照时刻确定 |
| **Lemma-S-17-04** | 无孤儿消息保证 | 04.01 | Consistent Cut |
| **Lemma-S-18-01** | Source可重放引理 | 04.02 | 无丢失证明 |
| **Lemma-S-18-02** | 2PC原子性引理 | 04.02 | 无重复证明 |
| **Lemma-S-18-03** | 状态恢复一致性引理 | 04.02 | 恢复正确性 |
| **Lemma-S-18-04** | 算子确定性引理 | 04.02 | 重放一致性 |
| **Lemma-S-19-01** | Marker传播不变式 | 04.03 | Thm-S-19-01 Part 1 |
| **Lemma-S-19-02** | 一致割集引理 | 04.03 | Thm-S-19-01 Part 2 |
| **Lemma-S-19-03** | 通道状态完备性 | 04.03 | 无消息丢失 |
| **Lemma-S-19-04** | 无孤儿消息保证 | 04.03 | Thm-S-19-01 Part 3 |

### 5.2 前沿层引理 (06-frontier)

| 引理编号 | 名称 | 位置 | 关键作用 |
|----------|------|------|----------|
| **Lemma-S-20-01** | Choreography组合性 | 06.02 | 并行组合保持良构 |
| **Lemma-S-20-02** | 投影保持活性 | 06.02 | 全局活性蕴含局部活性 |
| **Lemma-S-20-03** | 全局类型完备性 | 06.02 | 任意程序存在全局类型 |
| **Lemma-S-20-04** | 流计算确定性保持 | 06.02 | 投影后保持确定性 |
| **Lemma-S-25-01** | 表达能力与可验证性反向关系 | 06.01 | 可判定性单调递减 |
| **Lemma-S-25-02** | 动态拓扑验证复杂性下界 | 06.01 | ≥EXPSPACE下界 |
| **Lemma-S-29-01** | Agent投影保持性 | 06.03 | 规约下类型保持 |
| **Lemma-S-29-02** | LLM响应类型完备性 | 06.03 | supp(L(s))⊆{v\|⊢v:T} |
| **Lemma-S-29-03** | 多Agent合流性 | 06.03 | 不相交角色并行交换 |
| **Lemma-S-29-04** | 协议组合安全性 | 06.03 | 兼容系统安全组合 |
| **Lemma-S-06-03** | 路径规范化 | 06.04 | pDOT类型检查核心 |
| **Lemma-S-06-04** | 路径等价传递性 | 06.04 | ~TRANS规则保证 |
| **Lemma-S-06-01** | 进程参数化保持性 | first-person-choreographies | 替换保持良类型 |
| **Lemma-S-06-02** | CPC类型安全性 | first-person-choreographies | CPC规约无类型错误 |

### 5.3 工具层引理 (07-tools)

| 引理编号 | 名称 | 位置 | 关键作用 |
|----------|------|------|----------|
| **Lemma-S-07-01** | 时序逻辑属性分解 | 07-tools/tla-for-flink | Safety/Liveness分类 |
| **Lemma-S-07-01** | 分离合取分配律 | 07-tools/iris-separation-logic | P*(Q∨R) ⊢⊣ (P*Q)∨(P*R) |
| **Lemma-S-07-02** | 魔杖与分离伴随 | 07-tools/iris-separation-logic | *⊣⊣⊢ |
| **Lemma-S-07-03** | 不变式打开/关闭 | 07-tools/iris-separation-logic | Inv使用规则 |
| **Lemma-S-07-04** | 幽灵状态分配律 | 07-tools/iris-separation-logic | 份额组合规则 |
| **Lemma-S-07-05** | 持久性传播 | 07-tools/iris-separation-logic | □P ⊢⊣ P |
| **Lemma-S-07-06** | 高阶不变式不动点 | 07-tools/iris-separation-logic | HInv(ι,F) ⊢⊣ F(HInv) |
| **Lemma-S-07-04** | 归纳原理完备性 | 07-tools/coq-mechanization | T_ind语法完备 |
| **Lemma-S-07-01** | 模型检查完备性 | 07-tools/model-checking-practice | LTL/CTL可判定 |
| **Lemma-S-07-02** | 符号模型检查空间复杂度 | 07-tools/model-checking-practice | BDD O(log|S|) |

### 5.4 标准层引理 (08-standards)

| 引理编号 | 名称 | 位置 | 关键作用 |
|----------|------|------|----------|
| **Lemma-S-08-01** | 窗口函数闭包性 | 08-standards/streaming-sql-standard | f(S[W])⊆S[W] |
| **Lemma-S-08-02** | 流表转换幂等性 | 08-standards/streaming-sql-standard | Table→Stream→Table=Id |

---

## 6. 性质与推论注册表

| 编号 | 名称 | 位置 | 说明 |
|------|------|------|------|
| **Prop-S-08-01** | 端到端Exactly-Once分解 | 02.02 | Source ∧ Checkpoint ∧ Sink |
| **Prop-S-13-01** | 分区策略保持键局部性 | 03.02 | Hash分区保证 |
| **Prop-S-14-01** | 可判定性单调递减律 | 03.03 | L_i ⊂ L_j ⇒ Decidable(L_j) ⊆ Decidable(L_i) |
| **Prop-S-14-02** | 编码存在性保持不可判定性 | 03.03 | 不可判定性传递 |
| **Prop-S-17-01** | Barrier对齐与Exactly-Once关系 | 04.01 | 充分必要条件 |
| **Prop-S-18-01** | Checkpoint与2PC绑定关系 | 04.02 | 成功 ⟺ Commit |
| **Prop-S-18-02** | 观察等价性 | 04.02 | 故障执行 ≡ 理想执行 |
| **Cor-S-02-01** | 良类型会话进程无死锁 | 01.02 | Cut elimination |
| **Cor-S-07-01** | 容错一致性推论 | 02.01 | Checkpoint恢复保持确定性 |
| **Cor-S-14-01** | 可判定性递减推论 | 03.03 | Thm-S-14-01直接推论 |

### 6.2 前沿层性质与推论 (06-frontier)

| 编号 | 名称 | 位置 | 说明 |
|------|------|------|------|
| **Prop-S-25-01** | 近似验证充分性条件 | 06.01 | C1∧C2∧C3 ⇒ 概率保证 |
| **Prop-S-20-01** | Choreographic⊃传统数据流 | 06.02 | 表达能力严格包含 |
| **Prop-S-29-01** | Agent系统死锁自由 | 06.03 | 良类型MAST死锁自由 |
| **Prop-S-29-02** | 认知一致性保持 | 06.03 | 无K_p φ∧K_p ¬φ可满足 |
| **Prop-S-06-01** | 1CP表达力完备性 | first-person-choreographies | ℒ_MultiChor⊂ℒ_1CP |
| **Prop-S-06-02** | 类型良好性保持 | 06.04 | 规约保持子类型关系 |

### 6.3 工具层性质与推论 (07-tools)

| 编号 | 名称 | 位置 | 说明 |
|------|------|------|------|
| **Prop-S-07-01** | Checkpoint协议安全性 | 07-tools/tla-for-flink | completed⇒全部acked |
| **Prop-S-07-02** | Exactly-Once语义TLA+表达 | 07-tools/tla-for-flink | ◇completed∧原子提交 |
| **Prop-S-07-01** | Iris编码Actor模型 | 07-tools/iris-separation-logic | Mailbox(α)断言 |
| **Prop-S-07-02** | Session Types的Iris嵌入 | 07-tools/iris-separation-logic | !A.S ↦ ∃v.ℓ↦v*... |
| **Prop-S-07-03** | Iris与TLA+动作对应 | 07-tools/iris-separation-logic | Hoare↔Action对照 |
| **Prop-S-07-03** | Coq逻辑一致性 | 07-tools/coq-mechanization | 不存在⊢t:False |
| **Prop-S-07-05** | 提取计算正确性 | 07-tools/coq-mechanization | t↝v ⇒ extract(t)↝*extract(v) |
| **Prop-S-07-01** | 流计算可验证属性分类 | 07-tools/model-checking-practice | Safety/Liveness/Fairness |

### 6.4 标准层性质与推论 (08-standards)

| 编号 | 名称 | 位置 | 说明 |
|------|------|------|------|
| **Prop-S-08-01** | SQL:2011窗口函数完备性 | 08-standards/streaming-sql-standard | 五类窗口函数 |
| **Prop-S-08-02** | 时间语义一致性 | 08-standards/streaming-sql-standard | 事件时间顺序保持 |

---

## 7. 核心概念速查表

### 7.1 六层表达能力层次 (L1-L6)

```
L₆: Turing-Complete
    λ-calculus, Turing Machine
    Fully Undecidable
           ↑
L₅: Higher-Order  ─────────────────  HOπ, Ambient
    Process-as-Data                    Mostly Undecidable
           ↑
L₄: Mobile  ───────────────────────  π-calculus, Actor
    Dynamic Names                      Partially Decidable
           ↑
L₃: Process Algebra  ──────────────  CSP, CCS
    Static Names                       EXPTIME
           ↑
L₂: Context-Free  ─────────────────  PDA, BPA
    Single Stack                       PSPACE-Complete
           ↑
L₁: Regular  ──────────────────────  FSM, Regex
    Finite Control                     P-Complete
```

| 层次 | 名称 | 核心资源 | 代表模型 | 可判定性 | 分离问题 |
|------|------|----------|----------|----------|----------|
| **L₁** | Regular | 有限控制+有限数据 | FSM, 正则表达式 | P-完全 | - |
| **L₂** | Context-Free | 有限控制+单栈 | PDA, BPA | PSPACE-完全 | {aⁿbⁿ} 识别 |
| **L₃** | Process Algebra | 静态命名+同步通信 | CSP, CCS | EXPTIME | 并行交错 P‖Q |
| **L₄** | Mobile | 动态创建+名字传递 | π-演算, Actor | 部分不可判定 | (νa) 动态创建 |
| **L₅** | Higher-Order | 进程作为数据传递 | HOπ, Ambient | 大部分不可判定 | a⟨Q⟩ 进程传递 |
| **L₆** | Turing-Complete | 无限制递归+数据 | λ-演算, TM | 完全不可判定 | 通用图灵计算 |

### 7.2 一致性层级

| 级别 | 名称 | 定义 | 实现机制 |
|------|------|------|----------|
| **AM** | At-Most-Once | 效果计数 ≤ 1 | 去重/幂等 |
| **AL** | At-Least-Once | 效果计数 ≥ 1 | 重试/重放 |
| **EO** | Exactly-Once | 效果计数 = 1 | Source重放 + Checkpoint + 事务Sink |

**一致性格**:

```
       Strong ───┬─── Causal ───┬─── Eventual
                 │              │
       EO ───────┴─── AL ───────┴─── AM
```

### 7.3 模型编码关系

| 源模型 | 目标模型 | 编码存在 | 关系 | 位置 |
|--------|----------|----------|------|------|
| CCS | π-演算 | ✅ | CCS ⊂ π | 01.02 |
| CSP | π-演算 | ✅ | CSP ⊂ π | 01.02 |
| 受限Actor | CSP | ✅ | Actor|_R ⊂ CSP | 03.01 |
| 完整Actor | CSP | ❌ | 无界spawn不可编码 | 03.01 |
| Flink | π-演算 | ✅ | 带Checkpoint扩展 | 03.02 |
| Go-CSP-sync | CSP | ✅ | 迹等价 | 01.05 |
| Scala-Actor | π-演算 | ✅ | Actor ⊂ π | 03.03 |
| π-演算 | HOπ | ✅ | π ⊂ HOπ | 03.03 |
| CSP | Actor | ❌ | ⊥ (不可比较) | 03.03 |

---

## 8. 文档依赖图

### 8.1 层级依赖关系

```
                    理论基础层
    ┌───────────────┬───────────────┬───────────────┐
    │ Chandy-Lamport│Happens-Before │  进程代数     │
    │ 分布式快照    │  偏序关系      │ CCS/CSP/π     │
    └───────┬───────┴───────┬───────┴───────┬───────┘
            │               │               │
            ↓               ↓               ↓
    ┌───────────────────────────────────────────────────┐
    │                  01-foundation                     │
    │  ┌─────┬─────┬─────┬─────┬─────┐                  │
    │  │01.01│01.02│01.03│01.04│01.05│     01.06        │
    │  │USTM │进程 │Actor│Data │ CSP │    Petri网       │
    │  └─────┴──┬──┴──┬──┴──┬──┴──┬──┘                  │
    │           │     │     │     │                     │
    └───────────┼─────┼─────┼─────┼─────────────────────┘
                │     │     │     │
                ↓     ↓     ↓     ↓
    ┌───────────────────────────────────────────────────┐
    │                  02-properties                     │
    │         ┌─────┬─────┬─────┬─────┐                 │
    │         │02.01│02.02│02.03│02.04│      02.05      │
    │         │确定 │一致 │Water│活性 │      类型       │
    │         └─────┴──┬──┴─────┴─────┘      安全       │
    │                  │                                │
    └──────────────────┼────────────────────────────────┘
                       │
                       ↓
    ┌───────────────────────────────────────────────────┐
    │                03-relationships                    │
    │    ┌─────────┬─────────┬─────────┐                │
    │    │  03.01  │  03.02  │  03.03  │                │
    │    │Actor→  │Flink→  │表达能力 │                │
    │    │CSP编码 │π演算    │层次     │                │
    │    └─────────┴────┬────┴─────────┘                │
    │                   │                               │
    └───────────────────┼───────────────────────────────┘
                        │
                        ↓
    ┌───────────────────────────────────────────────────┐
    │                   04-proofs                        │
    │    ┌─────────┬─────────┬─────────┐                │
    │    │  04.01  │  04.02  │  04.03  │                │
    │    │Check-  │Exactly- │Chandy-  │                │
    │    │point   │Once     │Lamport  │                │
    │    └─────────┴─────────┴─────────┘                │
    └───────────────────────────────────────────────────┘
                            ↓
    ┌───────────────────────────────────────────────────┐
│                 05-comparative-analysis              │
│    ┌─────────────────────────────────────────┐       │
│    │                 05.01                   │       │
│    │              Go vs Scala                │       │
│    └─────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────┘
                            ↓
    ┌───────────────────────────────────────────────────┐
│                    06-frontier                       │
│    ┌─────────┬─────────┬─────────┬─────────┐         │
│    │  06.01  │  06.02  │  06.03  │  06.04  │         │
│    │ 开放问题│Choreo-  │AI Agent │  pDOT   │         │
│    │         │graphic │会话类型 │路径类型 │         │
│    └─────────┴────┬────┴────┬────┴────┬────┘         │
│                   │         │         │              │
└───────────────────┼─────────┼─────────┼──────────────┘
                    │         │         │
                    ↓         ↓         ↓
    ┌───────────────────────────────────────────────────┐
│                      07-tools                        │
│    ┌─────────┬─────────┬─────────┬─────────┐         │
│    │   Coq   │  TLA+   │  Iris   │ 模型检查│         │
│    │机械化证明│验证Flink│分离逻辑 │  实践   │         │
│    └─────────┴─────────┴─────────┴─────────┘         │
└─────────────────────────────────────────────────────┘
                            ↓
    ┌───────────────────────────────────────────────────┐
│                    08-standards                      │
│    ┌─────────────────────────────────────────┐       │
│    │         streaming-sql-standard          │       │
│    │              流式SQL标准                 │       │
│    └─────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────┘
```

### 8.2 跨层依赖关系

```
01-foundation ─────────────────────────────────────────┐
   │                                                   │
   ├──→ 06-frontier/06.04-pdot (类型理论基础)          │
   ├──→ 07-tools/iris (分离逻辑基础)                   │
   └──→ 08-standards (SQL类型系统)                     │
                                                       ↓
02-properties ─────────────────────────┐         应用与工具层
   │                                    │              │
   ├──→ 06-frontier/06.01 (验证性质)    │              │
   └──→ 06-frontier/06.03 (类型安全)    │              │
                                        │              │
03-relationships ─────┐                 │              │
   │                   │                 │              │
   ├──→ 06.02 (Choreographic编码)       │              │
   └──→ 06.03 (Agent通信协议)           │              │
                                        │              │
04-proofs ─────────────────────────────┼──────────────┘
   │                                    │
   ├──→ 06.01 (开放验证问题)            │
   ├──→ 07-tools/tla-for-flink          │
   └──→ 07-tools/coq-mechanization      │
                                        │
05-comparative ─────────────────────────┘
   │
   └──→ 06.04 (Scala 3类型系统)
```

---

## 9. 推荐阅读路径

### 9.1 研究者路径 (Researcher)

**目标**: 理解理论基础，掌握证明技术，能够扩展理论

```
第一阶段：理论基础 (1-2周)
├── 01.02 进程演算基础 ────────┐
├── 01.01 USTM统一理论 ────────┤→ 理解元模型和层次结构
└── 03.03 表达能力层次定理 ────┘

第二阶段：核心性质证明 (2-3周)
├── 02.01 确定性定理 ──────────┐
├── 02.02 一致性层次 ──────────┤→ 掌握形式化证明方法
├── 02.03 Watermark单调性 ─────┤
└── 02.04 活性与安全性 ────────┘

第三阶段：编码与关系 (1-2周)
├── 03.01 Actor→CSP编码 ───────┐
├── 03.02 Flink→进程演算 ──────┤→ 理解模型间映射
└── 01.05 CSP形式化 ───────────┘

第四阶段：正确性证明 (2-3周)
├── 04.03 Chandy-Lamport ──────┐
├── 04.01 Checkpoint正确性 ────┤→ 掌握分布式证明技术
└── 04.02 Exactly-Once正确性 ──┘
```

### 9.2 工程师路径 (Engineer)

**目标**: 掌握模型映射，能够设计可靠系统

```
快速通道 (1周)
├── 01.01 USTM统一理论 ────────┐
└── 01.04 Dataflow形式化 ──────┘→ 理解Flink理论基础

实践导向 (2-3周)
├── 02.02 一致性层次 ──────────┐→ 选择合适的一致性级别
├── 03.02 Flink→进程演算 ──────┤→ 理解Flink形式化语义
├── 04.01 Checkpoint正确性 ────┤→ 理解容错机制设计
└── 04.02 Exactly-Once正确性 ──┘→ 设计端到端一致系统

对比参考 (可选)
└── 05.01 Go vs Scala ─────────→ 语言选型参考
```

### 9.3 学生路径 (Student)

**目标**: 循序渐进建立完整知识体系

```
基础阶段 (3-4周)
├── 01.02 进程演算基础 ────────┐
│   ├── CCS语法 ───────────────┤
│   ├── CSP语法 ───────────────┤
│   └── π-演算 ────────────────┤
├── 01.03 Actor模型 ───────────┤→ 理解并发计算模型
├── 01.05 CSP形式化 ───────────┤
└── 01.06 Petri网 ─────────────┘

进阶阶段 (2-3周)
├── 01.01 USTM统一理论 ────────┐
├── 02.01 确定性 ──────────────┤→ 理解流计算性质
├── 02.02 一致性层次 ──────────┤
└── 03.03 表达能力层次 ────────┘

高级阶段 (2-3周)
├── 03.01 Actor→CSP编码 ───────┐
├── 03.02 Flink→进程演算 ──────┤→ 理解模型编码技术
└── 04-proofs/ ────────────────┘→ 学习形式化证明
```

### 9.4 前沿探索路径 (Frontier Explorer)

**目标**: 探索流计算理论前沿，开展创新研究

```
第一阶段：Choreographic编程 (2-3周)
├── 06.02 Choreographic流编程 ───┐
├── 06.03 AI Agent与会话类型 ─────┤→ 全局视角与类型驱动
└── first-person-choreographies ────┘

第二阶段：形式化工具实践 (2-3周)
├── 07-tools/coq-mechanization ────┐
├── 07-tools/tla-for-flink ────────┤→ 掌握验证工具链
└── 07-tools/iris-separation-logic ─┘

第三阶段：开放问题研究 (持续)
├── 06.01 流计算验证开放问题 ────┐→ 寻找研究切入点
└── 06.04 pDOT路径依赖类型 ────────┘→ 类型系统前沿
```

---

## 10. 关键结果汇总

### 10.1 核心理论结果

| 结果 | 定理 | 意义 |
|------|------|------|
| **表达能力严格层次** | Thm-S-14-01 | L₁ ⊂ L₂ ⊂ L₃ ⊂ L₄ ⊂ L₅ ⊆ L₆ |
| **CSP与π关系** | Thm-S-02-01 | CSP ⊂ π-calculus（严格包含） |
| **受限Actor可编码到CSP** | Thm-S-12-01 | 无动态地址传递时可保持迹语义 |
| **流计算确定性** | Thm-S-07-01 | 纯函数+FIFO+事件时间 → 确定性 |
| **Checkpoint一致性** | Thm-S-17-01 | Barrier对齐保证一致割集 |
| **端到端Exactly-Once** | Thm-S-18-01 | Source ∧ Checkpoint ∧ 事务Sink |
| **Chandy-Lamport正确性** | Thm-S-19-01 | Marker协议产生一致全局状态 |
| **Choreographic流程序正确性** | Thm-S-20-01 | 全局类型保证通信安全+死锁自由 |
| **AI Agent系统死锁自由** | Thm-S-29-01 | MAST类型系统保证Agent协调安全 |
| **1CP死锁自由保证** | Thm-S-06-01 | 进程参数化Choreography死锁自由 |
| **pDOT类型安全性** | Thm-S-06-01 | 路径依赖类型Progress+Preservation |
| **SQL:2011窗口函数流正确性** | Thm-S-08-01 | 窗口函数语义可无损迁移至流处理 |

### 10.2 工程指导原则

| 场景 | 推荐模型 | 理由 |
|------|----------|------|
| 静态拓扑验证 | CSP (L₃) | 可判定，FDR等工具支持 |
| 动态微服务 | Actor/π (L₄) | 支持动态拓扑，需运行时监控 |
| 流处理容错 | Dataflow+Checkpoint | Thm-S-17-01保证一致性 |
| 端到端一致性 | Exactly-Once (L₅) | Thm-S-18-01三要素合取 |
| 安全关键系统 | L₁-L₂ | 完全可判定，可自动验证 |

### 10.3 开放问题

1. **L₅ ⊂ L₆ 的严格性**: HOπ是否严格弱于图灵完备？（已知HOπ是图灵完备的）
2. **异步vs同步π**: Palamidessi定理的扩展（混合选择不可编码性）
3. **流计算类型系统**: 带事件时间和窗口的类型安全证明
4. **容错复杂度**: Checkpoint算法在动态拓扑下的复杂度边界

### 10.4 前沿研究进展 (06-frontier)

| 方向 | 核心成果 | 关键定理/定义 | 状态 |
|------|----------|---------------|------|
| **Choreographic流编程** | 全局类型推断、死锁自由保证 | Thm-S-20-01/02, Def-S-20-01~06 | Active |
| **AI Agent会话类型** | MAST框架、认知会话类型 | Thm-S-29-01, Def-S-29-01~06 | Active |
| **1CP第一人称编程** | 进程参数化、CPC通信 | Thm-S-06-01~03, Def-S-06-10~12 | Active |
| **pDOT路径依赖类型** | 任意长度路径、类型安全 | Thm-S-06-01, Def-S-06-07~10 | Active |
| **流计算验证开放问题** | 验证问题谱系、可判定性边界 | Def-S-25-01~04 | Tracking |

---

## 11. 文档清单

### 11.1 完整文档列表

```
Struct/
├── 00-INDEX.md                           [本文档 - 主索引]
├── 01-foundation/
│   ├── 01.01-unified-streaming-theory.md     [USTM统一理论, Thm-S-01-01/02]
│   ├── 01.02-process-calculus-primer.md      [进程演算基础, Thm-S-02-01]
│   ├── 01.03-actor-model-formalization.md    [Actor模型, Thm-S-03-01/02]
│   ├── 01.04-dataflow-model-formalization.md [Dataflow, Thm-S-04-01]
│   ├── 01.05-csp-formalization.md            [CSP, Thm-S-05-01]
│   └── 01.06-petri-net-formalization.md      [Petri网, Thm-S-06-01]
├── 02-properties/
│   ├── 02.01-determinism-in-streaming.md     [流计算确定性, Thm-S-07-01]
│   ├── 02.02-consistency-hierarchy.md        [一致性层次, Thm-S-08-01/02/03]
│   ├── 02.03-watermark-monotonicity.md       [Watermark单调性, Thm-S-09-01]
│   ├── 02.04-liveness-and-safety.md          [活性/安全性, Thm-S-10-01]
│   └── 02.05-type-safety-derivation.md       [类型安全, Thm-S-11-01]
├── 03-relationships/
│   ├── 03.01-actor-to-csp-encoding.md        [Actor→CSP编码, Thm-S-12-01]
│   ├── 03.02-flink-to-process-calculus.md    [Flink→π演算, Thm-S-13-01]
│   └── 03.03-expressiveness-hierarchy.md     [表达能力层次, Thm-S-14-01]
├── 04-proofs/
│   ├── 04.01-flink-checkpoint-correctness.md [Checkpoint正确性, Thm-S-17-01]
│   ├── 04.02-flink-exactly-once-correctness.md [Exactly-Once, Thm-S-18-01/02]
│   └── 04.03-chandy-lamport-consistency.md   [Chandy-Lamport, Thm-S-19-01]
├── 05-comparative-analysis/
│   └── 05.01-go-vs-scala-expressiveness.md   [Go vs Scala, Thm-S-24-01]
├── 06-frontier/                              [前沿研究方向]
│   ├── 06.01-open-problems-streaming-verification.md [开放问题, Def-S-25-01~04]
│   ├── 06.02-choreographic-streaming-programming.md  [Choreographic流编程, Thm-S-20-01/02]
│   ├── 06.03-ai-agent-session-types.md               [AI Agent与会话类型, Thm-S-29-01]
│   ├── 06.04-pdot-path-dependent-types.md            [pDOT路径依赖类型, Thm-S-06-01]
│   └── first-person-choreographies.md                [1CP第一人称Choreographic, Thm-S-06-01~03]
├── 07-tools/                                 [形式化工具]
│   ├── coq-mechanization.md                    [Coq机械化证明, Thm-S-07-01/02]
│   ├── tla-for-flink.md                        [TLA+验证Flink, Thm-S-07-01]
│   ├── iris-separation-logic.md                [Iris分离逻辑, Thm-S-07-01/02]
│   ├── model-checking-practice.md              [模型检查实践, Prop-S-07-01]
│   └── smart-casual-verification.md            [Smart Casual验证, Def-S-07-13~16]
└── 08-standards/                             [标准规范]
    └── streaming-sql-standard.md               [流式SQL标准, Thm-S-08-01]
```

### 11.2 文档统计

| 类别 | 数量 | 总定理 | 总定义 | 总引理 |
|------|------|--------|--------|--------|
| 01-foundation | 6 | 7 | 14 | 5 |
| 02-properties | 5 | 5 | 12 | 6 |
| 03-relationships | 3 | 4 | 11 | 6 |
| 04-proofs | 3 | 4 | 15 | 12 |
| 05-comparative | 1 | 1 | 4 | 4 |
| **总计** | **18** | **21** | **56** | **33** |

### 11.3 新增前沿与工具文档 (06-08)

| 类别 | 数量 | 总定理 | 总定义 | 总引理 |
|------|------|--------|--------|--------|
| 06-frontier | 5 | 7 | 23 | 12 |
| 07-tools | 5 | 2 | 18 | 8 |
| 08-standards | 1 | 1 | 3 | 2 |
| **新文档总计** | **11** | **10** | **44** | **22** |

### 11.4 更新后完整统计

| 类别 | 数量 | 总定理 | 总定义 | 总引理 |
|------|------|--------|--------|--------|
| 01-foundation | 6 | 7 | 14 | 5 |
| 02-properties | 5 | 5 | 12 | 6 |
| 03-relationships | 3 | 4 | 11 | 6 |
| 04-proofs | 3 | 4 | 15 | 12 |
| 05-comparative | 1 | 1 | 4 | 4 |
| 06-frontier | 5 | 7 | 23 | 12 |
| 07-tools | 5 | 2 | 18 | 8 |
| 08-standards | 1 | 1 | 3 | 2 |
| **总计** | **29** | **31** | **100** | **55** |

---

*索引创建时间: 2026-04-02*
*适用项目: AnalysisDataFlow/Struct*
*维护建议: 新增文档后更新定理/定义/引理注册表和依赖图*
