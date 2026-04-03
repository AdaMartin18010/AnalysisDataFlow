# 形式化验证工具选择决策树

> 所属阶段: visuals/ | 前置依赖: [Struct/07-tools/tla-for-flink.md](../Struct/07-tools/tla-for-flink.md), [Struct/07-tools/coq-mechanization.md](../Struct/07-tools/coq-mechanization.md), [Struct/07-tools/iris-separation-logic.md](../Struct/07-tools/iris-separation-logic.md), [Struct/07-tools/smart-casual-verification.md](../Struct/07-tools/smart-casual-verification.md) | 形式化等级: L4-L6

---

## 1. 概念定义 (Definitions)

### Def-V-01-01: 形式化验证方法谱系

**定义 (Formal Verification Spectrum)**:

形式化验证方法按其严格程度和工程成本形成连续谱系：

$$
\text{VerificationMethod} ::= \underbrace{\text{Testing}}_{\text{轻量}} \mid \underbrace{\text{Smart Casual}}_{\text{混合}} \mid \underbrace{\text{Model Checking}}_{\text{自动}} \mid \underbrace{\text{Theorem Proving}}_{\text{严格}}
$$

各方法的核心特征：

| 方法类型 | 自动化程度 | 数学保证 | 适用规模 | 学习曲线 |
|----------|-----------|----------|----------|----------|
| 传统测试 | ★★★★★ | ★☆☆☆☆ | 任意 | 平缓 |
| Smart Casual Verification | ★★★★☆ | ★★★☆☆ | 大型 | 中等 |
| 模型检验 (TLA+/SPIN) | ★★★☆☆ | ★★★★☆ | 中型 | 中等 |
| 定理证明 (Coq/Iris) | ★★☆☆☆ | ★★★★★ | 小型核心 | 陡峭 |

---

### Def-V-01-02: 验证目标分类

**定义 (Verification Objectives)**:

形式化验证关注的三类核心性质：

$$
\begin{aligned}
\text{安全性(Safety)} &\triangleq \Box \neg \text{BadThing} \quad \text{"永远不应发生"} \\
\text{活性(Liveness)} &\triangleq \Box \Diamond \text{GoodThing} \quad \text{"最终必须发生"} \\
\text{功能正确性} &\triangleq \forall \text{input}.\ \text{Spec}(\text{input}, \text{output})
\end{aligned}
$$

**流计算典型性质映射**：

| 性质类别 | Flink示例 | 形式化表达 |
|----------|-----------|------------|
| 安全性 | Checkpoint一致性 | $\Box(\text{completed}(c) \Rightarrow \forall t: \text{acked}(t,c))$ |
| 活性 | 水印最终推进 | $\Diamond(\text{watermark} = T_{\max})$ |
| 功能正确性 | Exactly-Once语义 | $\forall r: \text{processed}(r) = 1$ |

---

## 2. 决策树可视化

### 2.1 形式化验证工具选择决策树 (完整版)

以下决策树帮助根据项目特征选择最合适的形式化验证工具：

```mermaid
flowchart TD
    Start([开始选择]) --> Goal{验证目标?}

    %% 第一层：验证目标
    Goal -->|Safety/安全性| Proof{需要机械证明?}
    Goal -->|Liveness/活性| Scale1{系统规模?}
    Goal -->|功能正确性| Fam1{团队熟悉度?}

    %% Safety分支
    Proof -->|是| Scale2{系统规模?}
    Proof -->|否| SCV1[Smart Casual Verification]

    Scale2 -->|小型<br/><1000 LoC| Coq[Coq证明助手]
    Scale2 -->|中型| TLA1[TLA+ + TLC]
    Scale2 -->|大型| SCV2[Smart Casual Verification]

    %% Liveness分支
    Scale1 -->|小型| TLA2[TLA+ + TLC]
    Scale1 -->|中型| Realtime1{时间约束?}
    Scale1 -->|大型| SCV3[Smart Casual Verification]

    Realtime1 -->|实时| TLA3[TLA+ + TLC]
    Realtime1 -->|非实时| MC1[Model Checking<br/>SPIN/Promela]

    %% 功能正确性分支
    Fam1 -->|高| Coq2[Coq + 代码提取]
    Fam1 -->|中| Scale3{系统规模?}
    Fam1 -->|低| SCV4[Smart Casual Verification]

    Scale3 -->|小型| Coq3[Coq证明助手]
    Scale3 -->|中型| TLA4[TLA+ + TLC]
    Scale3 -->|大型| SCV5[Smart Casual Verification]

    %% 特殊分支：并发程序验证
    Goal -->|细粒度并发| Fam2{团队熟悉度?}
    Fam2 -->|高| Iris[Iris分离逻辑]
    Fam2 -->|中| SCV6[Smart Casual Verification]
    Fam2 -->|低| TLA5[TLA+ + TLC]

    %% 样式定义
    style Start fill:#e3f2fd
    style Goal fill:#fff3e0
    style Proof fill:#fff3e0
    style Scale1 fill:#fff3e0
    style Scale2 fill:#fff3e0
    style Scale3 fill:#fff3e0
    style Fam1 fill:#fff3e0
    style Fam2 fill:#fff3e0
    style Realtime1 fill:#fff3e0

    style Coq fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style Coq2 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style Coq3 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style TLA1 fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style TLA2 fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style TLA3 fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style TLA4 fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style TLA5 fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Iris fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    style SCV1 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style SCV2 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style SCV3 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style SCV4 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style SCV5 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style SCV6 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style MC1 fill:#fff8e1,stroke:#f57f17,stroke-width:2px
```

---

### 2.2 简化快速决策树

```mermaid
flowchart TD
    A([选择形式化工具]) --> B{项目阶段?}

    B -->|设计阶段| C{协议复杂度?}
    B -->|实现阶段| D{团队经验?}
    B -->|维护阶段| E[Smart Casual Verification]

    C -->|简单| F[TLA+快速建模]
    C -->|复杂| G{需要100%保证?}

    G -->|是| H[Coq/Iris全程证明]
    G -->|否| I[TLA+ + TLC]

    D -->|丰富| J{目标代码量?}
    D -->|有限| K[Smart Casual Verification]

    J -->|<5K行| L[Coq提取代码]
    J -->|>5K行| M[TLA+规格 + Trace验证]

    style E fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style K fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style H fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style L fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style F fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style I fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style M fill:#e1f5fe,stroke:#01579b,stroke-width:2px
```

---

## 3. 工具详细对比

### 3.1 工具特性矩阵

| 特性维度 | TLA+ | Coq | Iris | Smart Casual | SPIN |
|----------|------|-----|------|--------------|------|
| **逻辑基础** | ZFC + 时序逻辑 | CIC (依赖类型) | 高阶并发分离逻辑 | TLA+ + Trace检查 | LTL + 自动机 |
| **证明方式** | 模型检验(TLC) | 交互式策略 | 交互式+自动化 | 自动化 | 模型检验 |
| **并发支持** | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ | ★★★★☆ |
| **活性验证** | 原生支持 | 需嵌入 | 支持 | 支持 | 原生支持 |
| **代码提取** | 无 | OCaml/Haskell | 无 | 无 | 无 |
| **学习周期** | 2-4周 | 3-6月 | 4-8月 | 1-2周 | 1-2周 |
| **工业案例** | AWS/Azure | CompCert/VST | RustBelt | Microsoft CCF | 协议验证 |

---

### 3.2 各工具详细说明

#### TLA+ / PlusCal

**学习曲线**: ★★★☆☆ (中等)

**适用场景**:

- 分布式协议设计验证 (Raft/Paxos/Checkpoint)
- 安全性与活性属性验证
- 大规模状态空间探索

**代表案例**:

| 项目 | 验证内容 | 成果 |
|------|----------|------|
| AWS DynamoDB | 分布式事务协议 | 发现3个关键设计缺陷[^1] |
| Microsoft CCF | 共识协议 | 发现6个bug (4设计+2实现)[^2] |
| Flink Checkpoint | Barrier对齐协议 | 精化验证实现正确性 |

**工具链**:

- TLC: 模型检验器
- TLAPS: 证明辅助系统
- PlusCal: 伪代码风格算法语言

**核心优势**: 时序逻辑原生支持、状态空间可视化、工业界广泛采用

---

#### Coq 证明助手

**学习曲线**: ★★★★★ (陡峭)

**适用场景**:

- 核心算法函数式实现与验证
- 需要代码提取到生产环境
- 数学级严格正确性保证

**代表案例**:

| 项目 | 规模 | 成果 |
|------|------|------|
| CompCert C编译器 | 10万+行Coq | 生成二进制与C语义等价保证[^3] |
| VST (Verified Software Toolchain) | 大规模 | C程序分离逻辑验证 |
| Fiat-Crypto | 密码学原语 | 生成经验证的加密代码 |

**核心优势**: 依赖类型精确表达、可提取可执行代码、逻辑一致性保证

**限制**: 学习曲线陡峭、不适合大规模系统全验证

---

#### Iris 分离逻辑

**学习曲线**: ★★★★★ (陡峭)

**适用场景**:

- 细粒度并发数据结构验证
- 高阶并发程序 (Rust/Go)
- 资源管理与所有权推理

**代表案例**:

| 项目 | 验证内容 | 成果 |
|------|----------|------|
| RustBelt | Rust标准库 | 验证内存安全原语[^4] |
| IronFleet | 分布式系统 | 端到端活性证明 |
| 并发行波器 | 算子组合 | 分离合取组合规范 |

**核心概念**:

- 分离合取 ($*$): 资源不相交组合
- 不变式 (Inv): 共享资源协议
- 幽灵状态: 验证时辅助推理状态

**核心优势**: 模块化并发推理、支持逻辑原子性、与类型系统结合

---

#### Smart Casual Verification

**学习曲线**: ★★★☆☆ (中等偏低)

**适用场景**:

- 大型分布式系统持续验证
- 团队形式化经验有限
- 需要快速ROI的项目

**核心组成**:

$$
\text{SCV} = \underbrace{\text{TLA+规格}}_{\text{真理源}} + \underbrace{\text{TLC模型检验}}_{\text{设计验证}} + \underbrace{\text{Trace验证}}_{\text{实现一致性}}
$$

**代表案例 - Microsoft CCF**:

- 2工程师 × 3周 = 约240人时投入
- 发现6个关键bug（含2个生产级严重缺陷）
- ROI ≈ 317%

**核心优势**:

- 工程成本与收益平衡
- 可集成CI/CD持续验证
- 分布式团队可掌握

**局限性**: 不完备保证、依赖测试覆盖率

---

## 4. 工具选择决策框架

### 4.1 决策维度详解

```mermaid
graph TB
    subgraph "决策维度权重分析"
        A[验证目标] --> A1[安全性: TLA+/Coq优先]
        A --> A2[活性: TLA+优先]
        A --> A3[功能: Coq优先]

        B[机械证明需求] --> B1[是: Coq/Iris]
        B --> B2[否: TLA+/SCV]

        C[系统规模] --> C1[小: 任意工具]
        C --> C2[中: TLA+/MC]
        C --> C3[大: SCV必选]

        D[时间约束] --> D1[实时: TLA+]
        D --> D2[非实时: MC可选]

        E[团队熟悉度] --> E1[高: Coq/Iris]
        E --> E2[中: TLA+]
        E --> E3[低: SCV]
    end
```

### 4.2 推荐决策路径

| 场景描述 | 推荐工具 | 预期投入 | 预期产出 |
|----------|----------|----------|----------|
| 初创团队，验证关键协议设计 | TLA+ | 2-4周 | 设计缺陷早期发现 |
| 成熟团队，验证核心算法 | Coq | 2-4月 | 经证明的参考实现 |
| 细粒度并发优化 | Iris | 2-3月 | 无数据竞争保证 |
| 大型系统持续验证 | SCV | 1-2周启动 | CI集成验证流水线 |
| 快速原型验证 | Smart Casual | 1周内 | 轻量级规格约束 |

---

## 5. 流计算系统验证建议

### 5.1 Flink组件映射

| Flink组件 | 验证目标 | 推荐工具 | 关键性质 |
|-----------|----------|----------|----------|
| Checkpoint协议 | 安全性 | TLA+/SCV | 所有任务最终确认 |
| Barrier对齐 | 安全性+活性 | TLA+ | 无数据丢失 |
| Watermark传播 | 活性 | TLA+ | 单调推进 |
| Exactly-Once | 功能正确性 | Coq/SCV | 原子提交 |
| State Backend | 安全性 | Iris/SCV | 快照一致性 |
| 动态扩缩容 | 安全性 | TLA+ | 状态不丢失 |

### 5.2 实施路线图建议

```mermaid
gantt
    title 形式化验证实施路线图
    dateFormat YYYY-MM

    section 阶段1: 基础
    选择验证方法           :a1, 2026-01, 1w
    TLA+培训              :a2, after a1, 2w
    Checkpoint规格建模     :a3, after a2, 3w

    section 阶段2: 验证
    TLC模型检验           :b1, after a3, 2w
    Trace收集工具开发      :b2, after a3, 2w
    Smart Casual集成       :b3, after b1, 2w

    section 阶段3: 扩展
    Watermark验证         :c1, after b3, 2w
    Exactly-Once规格       :c2, after b3, 3w
    CI/CD集成             :c3, after c2, 2w
```

---

## 6. 可视化总结

### 6.1 工具-场景匹配矩阵

```mermaid
graph LR
    subgraph "工具选择矩阵"
        direction TB

        V1[高保证需求] --- T1[Coq/Iris]
        V2[快速验证] --- T2[TLA+]
        V3[大型系统] --- T3[Smart Casual]
        V4[协议设计] --- T4[TLA+/MC]
        V5[代码提取] --- T5[Coq]
        V6[并发优化] --- T6[Iris]

        T1 --- C1[CompCert级别]
        T2 --- C2[AWS/Azure级别]
        T3 --- C3[CCF级别]
        T4 --- C4[Raft/Paxos级别]
        T5 --- C5[加密原语级别]
        T6 --- C6[RustBelt级别]
    end
```

### 6.2 投资回报对比

```mermaid
xychart-beta
    title "形式化验证方法: 投入vs回报"
    x-axis [投入成本]
    y-axis [验证保证] 0 --> 100

    line "传统测试" [[0], [20], [100]]
    line "SCV" [[10], [40], [60]]
    line "模型检验" [[30], [50], [80]]
    line "定理证明" [[60], [80], [100]]

    annotation "最佳ROI点" 30, 60
```

---

## 7. 引用参考 (References)

[^1]: C. Newcombe et al., "How Amazon Web Services Uses Formal Methods," *Communications of the ACM*, 58(4), 2015. <https://doi.org/10.1145/2699417>

[^2]: H. Howard et al., "Smart Casual Verification of the Confidential Consortium Framework," *NSDI 2025*, 2025. <https://www.usenix.org/conference/nsdi25/presentation/howard>

[^3]: X. Leroy, "Formal Verification of a Realistic Compiler," *Communications of the ACM*, 52(7), 2009. <https://doi.org/10.1145/1538788.1538814>

[^4]: R. Jung et al., "RustBelt: Securing the Foundations of the Rust Programming Language," *POPL 2018*, 2018. <https://doi.org/10.1145/3158154>



---

*文档版本: 1.0 | 创建日期: 2026-04-03 | 状态: Complete*
