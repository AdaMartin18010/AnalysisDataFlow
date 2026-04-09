# USTM-F 文档依赖关系全景图

> **统一流计算理论元框架 - 文档交叉引用图谱**
> **版本**: v1.0 | **文档数**: 32 | **生成日期**: 2026-04-08

---

## 1. 五层架构依赖总图

```mermaid
graph TB
    subgraph "L0: 元理论基础 (00-meta/)"
        M1[00.01-category-theory-foundation.md<br/>Def-M-01~10]
        M2[00.02-lattice-order-theory.md<br/>Def-M-11~20, Thm-M-01~05]
        M3[00.03-type-theory-foundation.md<br/>Def-M-21~30]
        M0[00.00-ustm-f-overview.md<br/>Def-M-00, 31~33]
    end

    subgraph "L1: 统一流模型 (01-unified-model/)"
        U11[01.01-stream-mathematical-definition.md<br/>Def-U-01~10, Thm-U-01~02]
        U12[01.02-unified-time-model.md<br/>Def-U-11~20, Thm-U-03]
        U13[01.03-operator-algebra.md<br/>Def-U-21~30]
        U14[01.04-composition-theory.md<br/>Def-U-31~40, Thm-U-05~06]
        U15[01.05-ustm-core-semantics.md<br/>Def-U-41~50, Thm-U-03~04]
        U10[01.00-unified-streaming-theory-v2.md<br/>Def-U-51~58, Thm-U-07~08]
    end

    subgraph "L2: 模型实例化 (02-model-instantiation/)"
        I00[02.00-model-instantiation-framework.md<br/>Def-I-00-01~07, Thm-I-00-01~02]
        I01[02.01-actor-in-ustm.md<br/>Def-A-XX]
        I02[02.02-csp-in-ustm.md<br/>Def-C-XX]
        I03[02.03-dataflow-in-ustm.md<br/>Def-D-XX]
        I04[02.04-petri-net-in-ustm.md<br/>Def-P-XX]
        I05[02.05-pi-calculus-in-ustm.md<br/>Def-π-XX]
        I06[02.06-session-types-in-ustm.md<br/>Def-S-XX]
        I07[02.07-flink-in-ustm.md<br/>Def-F-XX]
    end

    subgraph "L3: 证明链 (03-proof-chains/)"
        P01[03.01-fundamental-lemmas.md<br/>Lemma-U-01~50]
        P02[03.02-determinism-theorem-proof.md<br/>Thm-U-20, Lemma-U-31~34]
        P03[03.03-consistency-lattice-theorem.md<br/>Thm-U-21~22]
        P04[03.04-watermark-monotonicity-proof.md<br/>Thm-U-25]
        P05[03.05-checkpoint-correctness-proof.md<br/>Thm-U-30]
        P06[03.06-exactly-once-semantics-proof.md<br/>Thm-U-35]
        P07[03.07-type-safety-proof.md<br/>Thm-U-36~38]
        P00[03.00-proof-chains-compendium.md<br/>证明链整合]
    end

    subgraph "L4: 编码与验证 (04-encoding-verification/)"
        E01[04.01-encoding-theory.md]
        E02[04.02-actor-csp-encoding.md]
        E03[04.03-dataflow-csp-encoding.md]
        E04[04.04-expressiveness-hierarchy-v2.md]
        E05[04.05-coq-formalization.md]
        E06[04.06-tla-plus-specifications.md]
    end

    %% L0 内部依赖
    M1 --> M0
    M2 --> M0
    M3 --> M0

    %% L0 -> L1
    M1 --> U11
    M2 --> U12
    M3 --> U15
    M0 --> U10

    %% L1 内部依赖
    U11 --> U12
    U11 --> U13
    U13 --> U14
    U12 --> U15
    U14 --> U15
    U11 --> U10
    U12 --> U10
    U13 --> U10
    U14 --> U10
    U15 --> U10

    %% L1 -> L2
    U10 --> I00
    U11 --> I01
    U11 --> I02
    U11 --> I03
    U11 --> I04
    U11 --> I05
    U15 --> I06
    U10 --> I07

    %% L2 内部依赖
    I00 --> I01
    I00 --> I02
    I00 --> I03
    I00 --> I04
    I00 --> I05
    I00 --> I06
    I00 --> I07

    %% L1/L2 -> L3
    U11 --> P01
    U13 --> P01
    U15 --> P01
    P01 --> P02
    P01 --> P03
    P01 --> P04
    P02 --> P05
    P03 --> P06
    P05 --> P06
    P01 --> P07
    P02 --> P00
    P03 --> P00
    P04 --> P00
    P05 --> P00
    P06 --> P00
    P07 --> P00

    %% L3 -> L4
    P02 --> E02
    P03 --> E04
    P05 --> E06
    P07 --> E05
    I02 --> E02
    I03 --> E03
    I00 --> E01
    I07 --> E06

    style M0 fill:#e3f2fd,stroke:#1565c0
    style U10 fill:#e8f5e9,stroke:#2e7d32
    style I00 fill:#fff3e0,stroke:#ef6c00
    style P00 fill:#fce4ec,stroke:#c2185b
    style E01 fill:#f3e5f5,stroke:#7b1fa2
```

---

## 2. 定理证明依赖链

```mermaid
graph TB
    subgraph "公理层"
        A1[Axiom-U-01<br/>流定义公理]
        A2[Axiom-U-02<br/>时间域公理]
        A3[Axiom-U-03<br/>算子定义公理]
        A4[Axiom-U-04<br/>类型系统公理]
    end

    subgraph "基础引理层"
        L01[Lemma-U-01~10<br/>流的代数性质]
        L11[Lemma-U-11~20<br/>时间性质]
        L21[Lemma-U-21~30<br/>算子组合性质]
        L31[Lemma-U-31~34<br/>确定性引理]
        L35[Lemma-U-35~37<br/>一致性引理]
        L38[Lemma-U-38~40<br/>Watermark引理]
        L41[Lemma-U-41~43<br/>Checkpoint引理]
        L44[Lemma-U-44~46<br/>Exactly-Once引理]
        L47[Lemma-U-47~50<br/>类型安全引理]
    end

    subgraph "核心定理层"
        T20[Thm-U-20<br/>流计算确定性定理]
        T21[Thm-U-21<br/>一致性格定理]
        T22[Thm-U-22<br/>一致性与延迟权衡]
        T25[Thm-U-25<br/>Watermark单调性定理]
        T30[Thm-U-30<br/>Checkpoint一致性定理]
        T35[Thm-U-35<br/>Exactly-Once语义定理]
        T36[Thm-U-36<br/>进展性定理]
        T37[Thm-U-37<br/>保持性定理]
        T38[Thm-U-38<br/>FG/FGG类型安全定理]
    end

    subgraph "应用层"
        APP1[Flink正确性保证]
        APP2[Kafka Streams正确性]
        APP3[Spark Streaming正确性]
        APP4[通用流处理验证]
    end

    A1 --> L01
    A2 --> L11
    A3 --> L21
    A3 --> L31
    A2 --> L35
    A2 --> L38
    A3 --> L41
    A3 --> L44
    A4 --> L47

    L01 --> T20
    L21 --> T20
    L31 --> T20
    L11 --> T21
    L35 --> T21
    L35 --> T22
    L11 --> T25
    L38 --> T25
    L41 --> T30
    T20 --> T30
    T21 --> T30
    L44 --> T35
    T30 --> T35
    L47 --> T36
    L47 --> T37
    T36 --> T38
    T37 --> T38

    T20 --> APP1
    T30 --> APP1
    T35 --> APP1
    T38 --> APP1
    T35 --> APP2
    T35 --> APP3
    T38 --> APP4

    style A1 fill:#ffccbc,stroke:#d84315
    style A2 fill:#ffccbc,stroke:#d84315
    style A3 fill:#ffccbc,stroke:#d84315
    style A4 fill:#ffccbc,stroke:#d84315
    style T20 fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style T30 fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style T35 fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style T38 fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
```

---

## 3. 阶段内文档依赖

### 3.1 阶段一：元理论 (00-meta/)

| 文档 | 依赖 | 被依赖 |
|------|------|--------|
| 00.01-category-theory-foundation.md | - | 00.00, 01.01, 01.03, 01.05 |
| 00.02-lattice-order-theory.md | - | 00.00, 01.02, 01.04 |
| 00.03-type-theory-foundation.md | - | 00.00, 01.05 |
| 00.00-ustm-f-overview.md | 00.01~00.03 | 01.00 |

### 3.2 阶段二：统一流模型 (01-unified-model/)

| 文档 | 依赖 | 被依赖 |
|------|------|--------|
| 01.01-stream-mathematical-definition.md | 00.01 | 01.02, 01.03, 01.00, 03.01 |
| 01.02-unified-time-model.md | 01.01 | 01.05, 01.00, 03.01 |
| 01.03-operator-algebra.md | 01.01 | 01.04, 01.00, 03.01 |
| 01.04-composition-theory.md | 01.03 | 01.05, 01.00 |
| 01.05-ustm-core-semantics.md | 01.02, 01.04, 00.03 | 01.00, 03.01, 02.06 |
| 01.00-unified-streaming-theory-v2.md | 01.01~01.05 | 02.00, 02.07 |

### 3.3 阶段三：模型实例化 (02-model-instantiation/)

| 文档 | 依赖 | 被依赖 |
|------|------|--------|
| 02.00-model-instantiation-framework.md | 01.00 | 全部02.01~02.07, 04.01 |
| 02.01-actor-in-ustm.md | 02.00, 01.01 | 04.02 |
| 02.02-csp-in-ustm.md | 02.00, 01.01 | 04.02, 04.03 |
| 02.03-dataflow-in-ustm.md | 02.00, 01.01 | 04.03 |
| 02.04-petri-net-in-ustm.md | 02.00, 01.01 | - |
| 02.05-pi-calculus-in-ustm.md | 02.00, 01.01 | - |
| 02.06-session-types-in-ustm.md | 02.00, 01.05 | - |
| 02.07-flink-in-ustm.md | 02.00, 01.00 | 04.06 |

### 3.4 阶段四：证明链 (03-proof-chains/)

| 文档 | 依赖 | 被依赖 |
|------|------|--------|
| 03.01-fundamental-lemmas.md | 01.01, 01.03, 01.05 | 全部03.02~03.07, 03.00 |
| 03.02-determinism-theorem-proof.md | 03.01 | 03.05, 03.00, 04.02 |
| 03.03-consistency-lattice-theorem.md | 03.01 | 03.06, 03.00, 04.04 |
| 03.04-watermark-monotonicity-proof.md | 03.01 | 03.05, 03.00 |
| 03.05-checkpoint-correctness-proof.md | 03.01, 03.02 | 03.06, 03.00, 04.06 |
| 03.06-exactly-once-semantics-proof.md | 03.01, 03.03, 03.05 | 03.00 |
| 03.07-type-safety-proof.md | 03.01 | 03.00, 04.05 |
| 03.00-proof-chains-compendium.md | 03.01~03.07 | - |

### 3.5 阶段五：编码与验证 (04-encoding-verification/)

| 文档 | 依赖 | 被依赖 |
|------|------|--------|
| 04.01-encoding-theory.md | 02.00 | - |
| 04.02-actor-csp-encoding.md | 02.01, 02.02, 03.02 | - |
| 04.03-dataflow-csp-encoding.md | 02.03, 02.02 | - |
| 04.04-expressiveness-hierarchy-v2.md | 02.00, 03.03 | - |
| 04.05-coq-formalization.md | 03.07 | - |
| 04.06-tla-plus-specifications.md | 02.07, 03.05 | - |

---

## 4. 定理到证明文档的引用映射

| 定理编号 | 定理名称 | 证明文档 | 所在章节 |
|----------|----------|----------|----------|
| Thm-U-01 | 流CPO的代数结构 | 01.01-stream-mathematical-definition.md | §5 |
| Thm-U-02 | 流函子的单子性质 | 01.01-stream-mathematical-definition.md | §5 |
| Thm-U-03 | 操作语义与指称语义一致性 | 01.02-unified-time-model.md, 01.05-ustm-core-semantics.md | §5 |
| Thm-U-04 | USTM语义的组合性 | 01.05-ustm-core-semantics.md | §5 |
| Thm-U-05 | 算子互交换律 | 01.04-composition-theory.md | §5 |
| Thm-U-06 | 组合优化正确性 | 01.04-composition-theory.md | §5 |
| Thm-U-07 | USTM图灵完备性 | 01.00-unified-streaming-theory-v2.md | §5 |
| Thm-U-08 | USTM一致性 | 01.00-unified-streaming-theory-v2.md | §5 |
| **Thm-U-20** | **流计算确定性定理** | **03.02-determinism-theorem-proof.md** | **§5** |
| Thm-U-21 | 一致性格定理 | 03.03-consistency-lattice-theorem.md | §5 |
| Thm-U-22 | 一致性与延迟权衡 | 03.03-consistency-lattice-theorem.md | §5 |
| **Thm-U-25** | **Watermark单调性定理** | **03.04-watermark-monotonicity-proof.md** | **§5** |
| **Thm-U-30** | **Checkpoint一致性定理** | **03.05-checkpoint-correctness-proof.md** | **§5** |
| **Thm-U-35** | **Exactly-Once语义定理** | **03.06-exactly-once-semantics-proof.md** | **§5** |
| Thm-U-36 | 进展性定理 | 03.07-type-safety-proof.md | §5 |
| Thm-U-37 | 保持性定理 | 03.07-type-safety-proof.md | §5 |
| **Thm-U-38** | **FG/FGG类型安全定理** | **03.07-type-safety-proof.md** | **§5** |
| Thm-I-00-01 | 统一编码框架相容性 | 02.00-model-instantiation-framework.md | §5 |
| Thm-I-00-02 | 模型间编码可组合性 | 02.00-model-instantiation-framework.md | §5 |

---

## 5. 引理引用快速索引

### 5.1 基础引理库 (03.01-fundamental-lemmas.md)

| 引理范围 | 内容 | 引用文档 |
|----------|------|----------|
| Lemma-U-01~10 | 流的代数性质 | 01.01, 03.02 |
| Lemma-U-11~20 | 时间/Watermark性质 | 01.02, 03.04 |
| Lemma-U-21~30 | 算子组合性质 | 01.03, 03.02 |
| Lemma-U-31~34 | 确定性引理 | 03.02 |
| Lemma-U-35~37 | 一致性引理 | 03.03 |
| Lemma-U-38~40 | Watermark单调性引理 | 03.04 |
| Lemma-U-41~43 | Checkpoint引理 | 03.05 |
| Lemma-U-44~46 | Exactly-Once引理 | 03.06 |
| Lemma-U-47~50 | 类型安全引理 | 03.07 |

---

## 6. 关键路径分析

### 6.1 最长证明链

**类型安全证明链** (7步):

```
Axiom-U-04 → Lemma-U-47 → Lemma-U-48 → Lemma-U-49 → Thm-U-36 → Thm-U-37 → Thm-U-38 → APP
```

### 6.2 核心关键路径

**Checkpoint → Exactly-Once** (流处理容错基础):

```
Thm-U-20 + Thm-U-21 → Thm-U-30 → Thm-U-35 → Flink/Kafka正确性
```

### 6.3 文档阅读推荐路径

**初学者路径** (按层次递进):

```
00.01 → 01.01 → 02.00 → 03.00 → 04.01
```

**定理验证路径** (专注于证明):

```
03.01 → 03.02 → 03.05 → 03.06 → 03.07
```

**工程应用路径** (面向实现):

```
01.00 → 02.07 → 03.05 → 04.06
```

---

## 7. 交叉引用统计

| 类别 | 数量 | 说明 |
|------|------|------|
| 总文档数 | 32 | 5个阶段 |
| 形式化定义 | 200+ | Def-M/U/I/A/C/D/P/π/S/F |
| 定理 | 19 | Thm-M/U/I-XX |
| 引理 | 53+ | Lemma-U-XX |
| 内部链接 | 150+ | 文档间交叉引用 |
| 证明链 | 6 | 核心定理证明路径 |

---

*文档版本: v1.0 | USTM-F 重构项目 | 最后更新: 2026-04-08*
