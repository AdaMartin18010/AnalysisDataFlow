# 形式化定理依赖关系图谱

> **所属阶段**: Struct/Visualizations | **前置依赖**: [../Struct/00-INDEX.md](../Struct/00-INDEX.md), [../THEOREM-REGISTRY.md](../THEOREM-REGISTRY.md) | **形式化等级**: L4-L6

---

## 目录

- [形式化定理依赖关系图谱](#形式化定理依赖关系图谱)
  - [目录](#目录)
  - [1. 定理依赖总览图](#1-定理依赖总览图)
  - [2. 分组定理依赖图](#2-分组定理依赖图)
    - [2.1 Checkpoint正确性定理组](#21-checkpoint正确性定理组)
    - [2.2 Exactly-Once正确性定理组](#22-exactly-once正确性定理组)
    - [2.3 类型安全定理组](#23-类型安全定理组)
    - [2.4 Choreographic编程定理组](#24-choreographic编程定理组)
  - [3. 从基础定义到最终定理的推理链](#3-从基础定义到最终定理的推理链)
    - [3.1 Checkpoint一致性推理链](#31-checkpoint一致性推理链)
    - [3.2 Exactly-Once正确性推理链](#32-exactly-once正确性推理链)
    - [3.3 Chandy-Lamport一致性推理链](#33-chandy-lamport一致性推理链)
  - [4. 定理与工程实现映射](#4-定理与工程实现映射)
    - [4.1 理论-实践映射矩阵](#41-理论-实践映射矩阵)
    - [4.2 Flink实现对应表](#42-flink实现对应表)
  - [5. 定理查询索引](#5-定理查询索引)
    - [5.1 按形式化等级索引](#51-按形式化等级索引)
      - [L3 - 语法/操作语义层](#l3-语法操作语义层)
      - [L4 - 模型语义层](#l4-模型语义层)
      - [L5 - 正确性证明层](#l5-正确性证明层)
      - [L6 - 元理论/不可判定性层](#l6-元理论不可判定性层)
    - [5.2 按文档位置索引](#52-按文档位置索引)
    - [5.3 按依赖关系索引](#53-按依赖关系索引)
      - [依赖Checkpoint一致性的定理](#依赖checkpoint一致性的定理)
      - [依赖Chandy-Lamport的定理](#依赖chandy-lamport的定理)
  - [6. 核心定理速查卡](#6-核心定理速查卡)
    - [Thm-S-17-01: Flink Checkpoint一致性定理](#thm-s-17-01-flink-checkpoint一致性定理)
    - [Thm-S-18-01: Flink Exactly-Once正确性定理](#thm-s-18-01-flink-exactly-once正确性定理)
    - [Thm-S-19-01: Chandy-Lamport一致性定理](#thm-s-19-01-chandy-lamport一致性定理)
    - [Thm-S-20-01: Choreographic流程序正确性](#thm-s-20-01-choreographic流程序正确性)
  - [7. 引用参考](#7-引用参考)

---

## 1. 定理依赖总览图

**图说明**: 本图展示了AnalysisDataFlow项目核心定理之间的依赖关系网络。节点代表定理(Thm)、引理(Lemma)和定义(Def)，边代表依赖关系。颜色编码：紫色为定义，蓝色为引理，绿色为定理，粉色为工程应用。

```mermaid
graph TB
    subgraph "理论基础层"
        FIFO[FIFO通道语义] --> HB[Happens-Before关系]
        HB --> CC[Consistent Cut理论]
        CL[Chandy-Lamport算法] --> CC
    end

    subgraph "定义层 - 基础模型"
        D01[Def-S-01-01<br/>USTM六元组]
        D02[Def-S-02-03<br/>π-演算定义]
        D03[Def-S-03-01<br/>Actor模型]
        D04[Def-S-04-01<br/>Dataflow图]
        D05[Def-S-05-01<br/>CSP语法]
    end

    subgraph "定义层 - 核心性质"
        D08[Def-S-08-04<br/>Exactly-Once语义]
        D11[Def-S-11-02<br/>Featherweight Go]
        D17[Def-S-17-02<br/>一致全局状态]
        D18[Def-S-18-01<br/>Exactly-Once语义]
        D19[Def-S-19-02<br/>一致割集]
    end

    subgraph "引理层 - Checkpoint"
        L17_01[Lemma-S-17-01<br/>Barrier传播不变式]
        L17_02[Lemma-S-17-02<br/>状态一致性引理]
        L17_03[Lemma-S-17-03<br/>对齐点唯一性]
        L17_04[Lemma-S-17-04<br/>无孤儿消息保证]
    end

    subgraph "引理层 - Exactly-Once"
        L18_01[Lemma-S-18-01<br/>Source可重放引理]
        L18_02[Lemma-S-18-02<br/>2PC原子性引理]
        L18_03[Lemma-S-18-03<br/>状态恢复一致性引理]
        L18_04[Lemma-S-18-04<br/>算子确定性引理]
    end

    subgraph "引理层 - Chandy-Lamport"
        L19_01[Lemma-S-19-01<br/>Marker传播不变式]
        L19_02[Lemma-S-19-02<br/>一致割集引理]
        L19_03[Lemma-S-19-03<br/>通道状态完备性]
        L19_04[Lemma-S-19-04<br/>无孤儿消息保证]
    end

    subgraph "核心定理层"
        T17[Thm-S-17-01<br/>Flink Checkpoint<br/>一致性定理]
        T18[Thm-S-18-01<br/>Flink Exactly-Once<br/>正确性定理]
        T19[Thm-S-19-01<br/>Chandy-Lamport<br/>一致性定理]
        T11[Thm-S-11-01<br/>类型安全定理]
        T20[Thm-S-20-01<br/>Choreographic流程序<br/>正确性定理]
    end

    subgraph "工程应用层"
        E17[Flink Checkpoint机制]
        E18[端到端Exactly-Once]
        E19[分布式快照实现]
        E11[Go/Scala类型系统]
        E20[Choreographic编程]
    end

    %% 定义到引理的依赖
    D17 --> L17_01
    D17 --> L17_02
    D18 --> L18_01
    D18 --> L18_02
    D19 --> L19_01
    D19 --> L19_02

    %% 引理到定理的依赖
    L17_01 --> T17
    L17_02 --> T17
    L17_03 --> T17
    L17_04 --> T17

    L18_01 --> T18
    L18_02 --> T18
    L18_03 --> T18
    L18_04 --> T18

    L19_01 --> T19
    L19_02 --> T19
    L19_03 --> T19
    L19_04 --> T19

    %% 理论基础到定理
    CC --> T17
    CC --> T19
    HB --> T19

    %% 定理间依赖
    T17 --> T18
    T19 --> T17

    %% 定理到应用
    T17 --> E17
    T18 --> E18
    T19 --> E19
    T11 --> E11
    T20 --> E20

    %% 样式
    style FIFO fill:#fff9c4,stroke:#f57f17
    style HB fill:#fff9c4,stroke:#f57f17
    style CC fill:#fff9c4,stroke:#f57f17
    style CL fill:#fff9c4,stroke:#f57f17
    style D01 fill:#e1bee7,stroke:#6a1b9a
    style D02 fill:#e1bee7,stroke:#6a1b9a
    style D03 fill:#e1bee7,stroke:#6a1b9a
    style D04 fill:#e1bee7,stroke:#6a1b9a
    style D05 fill:#e1bee7,stroke:#6a1b9a
    style D08 fill:#e1bee7,stroke:#6a1b9a
    style D11 fill:#e1bee7,stroke:#6a1b9a
    style D17 fill:#e1bee7,stroke:#6a1b9a
    style D18 fill:#e1bee7,stroke:#6a1b9a
    style D19 fill:#e1bee7,stroke:#6a1b9a
    style L17_01 fill:#bbdefb,stroke:#1565c0
    style L17_02 fill:#bbdefb,stroke:#1565c0
    style L17_03 fill:#bbdefb,stroke:#1565c0
    style L17_04 fill:#bbdefb,stroke:#1565c0
    style L18_01 fill:#bbdefb,stroke:#1565c0
    style L18_02 fill:#bbdefb,stroke:#1565c0
    style L18_03 fill:#bbdefb,stroke:#1565c0
    style L18_04 fill:#bbdefb,stroke:#1565c0
    style L19_01 fill:#bbdefb,stroke:#1565c0
    style L19_02 fill:#bbdefb,stroke:#1565c0
    style L19_03 fill:#bbdefb,stroke:#1565c0
    style L19_04 fill:#bbdefb,stroke:#1565c0
    style T17 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style T18 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style T19 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style T11 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style T20 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style E17 fill:#f8bbd9,stroke:#ad1457
    style E18 fill:#f8bbd9,stroke:#ad1457
    style E19 fill:#f8bbd9,stroke:#ad1457
    style E11 fill:#f8bbd9,stroke:#ad1457
    style E20 fill:#f8bbd9,stroke:#ad1457
```

---

## 2. 分组定理依赖图

### 2.1 Checkpoint正确性定理组

**图说明**: 本组展示了Thm-S-17-01 (Flink Checkpoint一致性定理) 的完整依赖结构，从基础定义到工程应用。

```mermaid
graph TB
    subgraph "基础定义"
        D17_01[Def-S-17-01<br/>Checkpoint Barrier语义]
        D17_02[Def-S-17-02<br/>一致全局状态]
        D17_03[Def-S-17-03<br/>Checkpoint对齐]
        D17_04[Def-S-17-04<br/>状态快照原子性]
    end

    subgraph "支撑引理"
        L17_01[Lemma-S-17-01<br/>Barrier传播不变式]
        L17_02[Lemma-S-17-02<br/>状态一致性引理]
        L17_03[Lemma-S-17-03<br/>对齐点唯一性]
        L17_04[Lemma-S-17-04<br/>无孤儿消息保证]
    end

    subgraph "核心定理"
        T17[Thm-S-17-01<br/>Flink Checkpoint一致性定理]
    end

    subgraph "性质命题"
        P17_01[Prop-S-17-01<br/>Barrier对齐与Exactly-Once关系]
    end

    subgraph "工程实现"
        IMPL17_01[Barrier对齐机制]
        IMPL17_02[异步快照实现]
        IMPL17_03[状态后端一致性]
    end

    %% 依赖边
    D17_01 --> L17_01
    D17_02 --> L17_02
    D17_03 --> L17_01
    D17_03 --> L17_03
    D17_04 --> L17_04

    L17_01 --> T17
    L17_02 --> T17
    L17_03 --> T17
    L17_04 --> T17

    T17 --> P17_01
    T17 --> IMPL17_01
    T17 --> IMPL17_02
    T17 --> IMPL17_03

    %% 样式
    style D17_01 fill:#e1bee7,stroke:#6a1b9a
    style D17_02 fill:#e1bee7,stroke:#6a1b9a
    style D17_03 fill:#e1bee7,stroke:#6a1b9a
    style D17_04 fill:#e1bee7,stroke:#6a1b9a
    style L17_01 fill:#bbdefb,stroke:#1565c0
    style L17_02 fill:#bbdefb,stroke:#1565c0
    style L17_03 fill:#bbdefb,stroke:#1565c0
    style L17_04 fill:#bbdefb,stroke:#1565c0
    style T17 fill:#c8e6c9,stroke:#2e7d32,stroke-width:4px
    style P17_01 fill:#ffe0b2,stroke:#e65100
    style IMPL17_01 fill:#f8bbd9,stroke:#ad1457
    style IMPL17_02 fill:#f8bbd9,stroke:#ad1457
    style IMPL17_03 fill:#f8bbd9,stroke:#ad1457
```

### 2.2 Exactly-Once正确性定理组

**图说明**: 本组展示了Thm-S-18-01 (Flink Exactly-Once正确性定理) 及其依赖结构。

```mermaid
graph TB
    subgraph "基础定义"
        D18_01[Def-S-18-01<br/>Exactly-Once语义]
        D18_02[Def-S-18-02<br/>端到端一致性]
        D18_03[Def-S-18-03<br/>两阶段提交协议]
        D18_04[Def-S-18-04<br/>可重放Source]
        D18_05[Def-S-18-05<br/>幂等性]
    end

    subgraph "支撑引理"
        L18_01[Lemma-S-18-01<br/>Source可重放引理]
        L18_02[Lemma-S-18-02<br/>2PC原子性引理]
        L18_03[Lemma-S-18-03<br/>状态恢复一致性引理]
        L18_04[Lemma-S-18-04<br/>算子确定性引理]
    end

    subgraph "核心定理"
        T18_01[Thm-S-18-01<br/>Flink Exactly-Once<br/>正确性定理]
        T18_02[Thm-S-18-02<br/>幂等Sink等价性定理]
    end

    subgraph "性质命题"
        P18_01[Prop-S-18-01<br/>Checkpoint与2PC绑定关系]
        P18_02[Prop-S-18-02<br/>观察等价性]
    end

    subgraph "工程实现"
        IMPL18_01[TwoPhaseCommitSinkFunction]
        IMPL18_02[Kafka Exactly-Once Producer]
        IMPL18_03[幂等写入实现]
    end

    %% 依赖边
    D18_04 --> L18_01
    D18_03 --> L18_02
    D18_05 --> T18_02

    L18_01 --> T18_01
    L18_02 --> T18_01
    L18_03 --> T18_01
    L18_04 --> T18_01

    L18_01 --> T18_02
    L18_03 --> T18_02
    L18_04 --> T18_02

    T18_01 --> P18_01
    T18_01 --> P18_02

    T18_01 --> IMPL18_01
    T18_01 --> IMPL18_02
    T18_02 --> IMPL18_03

    %% 样式
    style D18_01 fill:#e1bee7,stroke:#6a1b9a
    style D18_02 fill:#e1bee7,stroke:#6a1b9a
    style D18_03 fill:#e1bee7,stroke:#6a1b9a
    style D18_04 fill:#e1bee7,stroke:#6a1b9a
    style D18_05 fill:#e1bee7,stroke:#6a1b9a
    style L18_01 fill:#bbdefb,stroke:#1565c0
    style L18_02 fill:#bbdefb,stroke:#1565c0
    style L18_03 fill:#bbdefb,stroke:#1565c0
    style L18_04 fill:#bbdefb,stroke:#1565c0
    style T18_01 fill:#c8e6c9,stroke:#2e7d32,stroke-width:4px
    style T18_02 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style P18_01 fill:#ffe0b2,stroke:#e65100
    style P18_02 fill:#ffe0b2,stroke:#e65100
    style IMPL18_01 fill:#f8bbd9,stroke:#ad1457
    style IMPL18_02 fill:#f8bbd9,stroke:#ad1457
    style IMPL18_03 fill:#f8bbd9,stroke:#ad1457
```

### 2.3 类型安全定理组

**图说明**: 本组展示了Thm-S-11-01 (类型安全定理) 及其相关定义和引理。

```mermaid
graph TB
    subgraph "基础定义"
        D11_02[Def-S-11-02<br/>Featherweight Go语法]
        D11_03[Def-S-11-03<br/>Generic Go语法]
        D11_04[Def-S-11-04<br/>DOT路径依赖类型]
    end

    subgraph "支撑引理"
        L11_01[Lemma-S-11-01<br/>替换引理]
    end

    subgraph "核心定理"
        T11[Thm-S-11-01<br/>类型安全<br/>Progress + Preservation]
    end

    subgraph "工程应用"
        IMPL11_01[Go编译器类型检查]
        IMPL11_02[Scala 3类型系统]
        IMPL11_03[Flink DataStream V2类型安全]
    end

    %% 依赖边
    D11_02 --> L11_01
    D11_03 --> L11_01

    L11_01 --> T11
    D11_02 --> T11
    D11_04 --> T11

    T11 --> IMPL11_01
    T11 --> IMPL11_02
    T11 --> IMPL11_03

    %% 样式
    style D11_02 fill:#e1bee7,stroke:#6a1b9a
    style D11_03 fill:#e1bee7,stroke:#6a1b9a
    style D11_04 fill:#e1bee7,stroke:#6a1b9a
    style L11_01 fill:#bbdefb,stroke:#1565c0
    style T11 fill:#c8e6c9,stroke:#2e7d32,stroke-width:4px
    style IMPL11_01 fill:#f8bbd9,stroke:#ad1457
    style IMPL11_02 fill:#f8bbd9,stroke:#ad1457
    style IMPL11_03 fill:#f8bbd9,stroke:#ad1457
```

### 2.4 Choreographic编程定理组

**图说明**: 本组展示了Thm-S-20-01 (Choreographic流程序正确性定理) 及其依赖结构。

```mermaid
graph TB
    subgraph "基础定义"
        D20_01[Def-S-20-01<br/>Choreographic编程核心概念]
        D20_02[Def-S-20-02<br/>Choreographic流程序]
        D20_03[Def-S-20-03<br/>多参与方会话类型MPST]
        D20_04[Def-S-20-04<br/>全局类型投影]
        D20_05[Def-S-20-05<br/>Choreographic Dataflow图]
        D20_06[Def-S-20-06<br/>全局类型推断系统]
    end

    subgraph "支撑引理"
        L20_01[Lemma-S-20-01<br/>Choreography组合性]
        L20_02[Lemma-S-20-02<br/>投影保持活性]
        L20_03[Lemma-S-20-03<br/>全局类型完备性]
        L20_04[Lemma-S-20-04<br/>流计算确定性保持]
    end

    subgraph "核心定理"
        T20_01[Thm-S-20-01<br/>Choreographic流程序正确性]
        T20_02[Thm-S-20-02<br/>全局类型推断完备性]
    end

    subgraph "性质命题"
        P20_01[Prop-S-20-01<br/>Choreographic⊃传统数据流]
    end

    subgraph "工程应用"
        IMPL20_01[Choral语言]
        IMPL20_02[MultiChor扩展]
        IMPL20_03[类型驱动流编程]
    end

    %% 依赖边
    D20_01 --> L20_01
    D20_03 --> L20_02
    D20_04 --> L20_02
    D20_06 --> L20_03
    D20_05 --> L20_04

    L20_01 --> T20_01
    L20_02 --> T20_01
    L20_04 --> T20_01

    L20_03 --> T20_02
    D20_06 --> T20_02

    T20_01 --> P20_01

    T20_01 --> IMPL20_01
    T20_01 --> IMPL20_02
    T20_01 --> IMPL20_03

    %% 样式
    style D20_01 fill:#e1bee7,stroke:#6a1b9a
    style D20_02 fill:#e1bee7,stroke:#6a1b9a
    style D20_03 fill:#e1bee7,stroke:#6a1b9a
    style D20_04 fill:#e1bee7,stroke:#6a1b9a
    style D20_05 fill:#e1bee7,stroke:#6a1b9a
    style D20_06 fill:#e1bee7,stroke:#6a1b9a
    style L20_01 fill:#bbdefb,stroke:#1565c0
    style L20_02 fill:#bbdefb,stroke:#1565c0
    style L20_03 fill:#bbdefb,stroke:#1565c0
    style L20_04 fill:#bbdefb,stroke:#1565c0
    style T20_01 fill:#c8e6c9,stroke:#2e7d32,stroke-width:4px
    style T20_02 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style P20_01 fill:#ffe0b2,stroke:#e65100
    style IMPL20_01 fill:#f8bbd9,stroke:#ad1457
    style IMPL20_02 fill:#f8bbd9,stroke:#ad1457
    style IMPL20_03 fill:#f8bbd9,stroke:#ad1457
```

---

## 3. 从基础定义到最终定理的推理链

### 3.1 Checkpoint一致性推理链

**推理链说明**: 本推理链展示了从基础定义到Thm-S-17-01的完整逻辑路径。

```
Def-S-17-01 (Checkpoint Barrier语义)
    ↓ 定义Barrier作为逻辑时间边界
Def-S-17-02 (一致全局状态)
    ↓ 定义全局状态需满足一致割集
Def-S-17-03 (Checkpoint对齐)
    ↓ 定义多输入算子Barrier同步机制
Lemma-S-17-01 (Barrier传播不变式)
    ↓ 证明Barrier传播保持因果封闭性
Lemma-S-17-02 (状态一致性引理)
    ↓ 证明对齐后快照构成一致状态
Lemma-S-17-03 (对齐点唯一性)
    ↓ 证明每个算子存在唯一对齐时刻
Lemma-S-17-04 (无孤儿消息保证)
    ↓ 证明快照中不存在孤儿消息
Thm-S-17-01 (Flink Checkpoint一致性定理)
    ↓ 综合上述结果
    ├─ Consistent(G_n): G_n对应一致割集
    ├─ NoOrphans(G_n): G_n中无孤儿消息
    └─ Reachable(G_n): G_n状态可达
```

### 3.2 Exactly-Once正确性推理链

```
Def-S-18-01 (Exactly-Once语义)
    ↓ 定义因果影响计数=1
Def-S-18-02 (端到端一致性)
    ↓ 分解为三要素合取
    ├─ Source可重放性
    ├─ Checkpoint一致性
    └─ Sink原子性
Def-S-18-03 (2PC协议)
    ↓ 定义两阶段提交语义
Def-S-18-04 (可重放Source)
    ↓ 定义Source确定性重放
Lemma-S-18-01 (Source可重放引理)
    ↓ 证明无丢失
Lemma-S-18-02 (2PC原子性引理)
    ↓ 证明无重复
Lemma-S-18-03 (状态恢复一致性引理)
    ↓ 证明恢复后状态一致
Lemma-S-18-04 (算子确定性引理)
    ↓ 证明重放产生相同输出
Thm-S-18-01 (Flink Exactly-Once正确性定理)
    ↓ 组合证明
    ├─ At-Least-Once (无丢失)
    ├─ At-Most-Once (无重复)
    └─ 合取得Exactly-Once
```

### 3.3 Chandy-Lamport一致性推理链

```
理论基础: Happens-Before关系 (Lamport 1978)
    ↓
理论基础: Consistent Cut定义
    ↓ 要求happens-before向下封闭
Def-S-19-01 (全局状态)
    ↓ 包含本地状态和通道状态
Def-S-19-02 (一致割集)
    ↓ 定义Consistent Cut条件
Def-S-19-03 (通道状态)
    ↓ 记录在途消息
Def-S-19-04 (Marker消息)
    ↓ 定义Marker作为快照边界
Lemma-S-19-01 (Marker传播不变式)
    ↓ Marker传播保持因果序
Lemma-S-19-02 (一致割集引理)
    ↓ Marker机制产生Consistent Cut
Lemma-S-19-03 (通道状态完备性)
    ↓ 记录在途消息无遗漏
Lemma-S-19-04 (无孤儿消息保证)
    ↓ 快照中无孤儿消息
Thm-S-19-01 (Chandy-Lamport一致性定理)
    ↓ 算法产生一致全局状态
```

---

## 4. 定理与工程实现映射

### 4.1 理论-实践映射矩阵

| 定理编号 | 理论保证 | 工程实现 | 适用系统 | 验证工具 |
|----------|----------|----------|----------|----------|
| **Thm-S-17-01** | Checkpoint一致性 | Barrier对齐、异步快照 | Flink, Spark Streaming | TLA+, Coq |
| **Thm-S-18-01** | Exactly-Once | 2PC Sink, 幂等写入 | Flink, Kafka Streams | Jepsen, TLA+ |
| **Thm-S-19-01** | 分布式快照一致性 | Marker协议 | Flink, Samza | TLA+ |
| **Thm-S-11-01** | 类型安全 | 编译器类型检查 | Go, Scala 3 | Coq, Isabelle |
| **Thm-S-20-01** | Choreographic正确性 | 全局类型推断 | Choral, MultiChor | 类型检查器 |
| **Thm-S-08-03** | 统一一致性格 | 一致性级别选择 | 所有流系统 | 模型检查 |
| **Thm-S-09-01** | Watermark单调性 | Watermark传播 | Flink, Beam | 时序逻辑 |
| **Thm-S-14-01** | 表达能力层次 | 模型选择 | Actor, CSP系统 | - |

### 4.2 Flink实现对应表

| 定理 | Flink组件 | 实现类/机制 | 验证方式 |
|------|-----------|-------------|----------|
| Thm-S-17-01 | Checkpoint机制 | `CheckpointCoordinator`<br/>`SubtaskCheckpointCoordinator` | 集成测试<br/>单元测试 |
| Thm-S-18-01 | Exactly-Once Sink | `TwoPhaseCommitSinkFunction`<br/>`FlinkKafkaProducer` | Jepsen测试<br/>端到端测试 |
| Thm-S-19-01 | Barrier传播 | `BarrierHandler`<br/>`CheckpointBarrier` | 模型检查<br/>TLA+规约 |
| Thm-S-09-01 | Watermark管理 | `WatermarkGenerator`<br/>`TimestampAssigner` | 单元测试 |
| Thm-S-07-01 | 确定性保证 | 纯函数算子<br/>事件时间处理 | 回归测试 |

---

## 5. 定理查询索引

### 5.1 按形式化等级索引

#### L3 - 语法/操作语义层

| 定理编号 | 名称 | 文档位置 |
|----------|------|----------|
| Thm-S-05-01 | Go-CS-sync ↔ CSP迹等价 | Struct/01-foundation/01.05 |
| Thm-S-11-01 | 类型安全(Progress + Preservation) | Struct/02-properties/02.05 |
| Thm-S-14-01 | 表达能力严格层次定理 | Struct/03-relationships/03.03 |

#### L4 - 模型语义层

| 定理编号 | 名称 | 文档位置 |
|----------|------|----------|
| Thm-S-01-01 | USTM组合性定理 | Struct/01-foundation/01.01 |
| Thm-S-03-01 | Actor局部确定性定理 | Struct/01-foundation/01.03 |
| Thm-S-04-01 | Dataflow确定性定理 | Struct/01-foundation/01.04 |
| Thm-S-07-01 | 流计算确定性定理 | Struct/02-properties/02.01 |
| Thm-S-08-03 | 统一一致性格 | Struct/02-properties/02.02 |
| Thm-S-09-01 | Watermark单调性定理 | Struct/02-properties/02.03 |
| Thm-S-12-01 | 受限Actor系统编码保持迹语义 | Struct/03-relationships/03.01 |

#### L5 - 正确性证明层

| 定理编号 | 名称 | 文档位置 |
|----------|------|----------|
| Thm-S-17-01 | Flink Checkpoint一致性定理 | Struct/04-proofs/04.01 |
| Thm-S-18-01 | Flink Exactly-Once正确性定理 | Struct/04-proofs/04.02 |
| Thm-S-18-02 | 幂等Sink等价性定理 | Struct/04-proofs/04.02 |
| Thm-S-19-01 | Chandy-Lamport一致性定理 | Struct/04-proofs/04.03 |
| Thm-S-20-01 | Choreographic流程序正确性 | Struct/04-proofs/04.07 |
| Thm-S-20-02 | 全局类型推断完备性 | Struct/04-proofs/04.07 |
| Thm-S-21-01 | FG/FGG类型安全定理 | Struct/04-proofs/04.05 |
| Thm-S-23-01 | Choreographic死锁自由定理 | Struct/04-proofs/04.07 |

#### L6 - 元理论/不可判定性层

| 定理编号 | 名称 | 文档位置 |
|----------|------|----------|
| Thm-S-22-01 | DOT子类型完备性定理 | Struct/04-proofs/04.06 |
| Thm-S-24-01 | Go与Scala图灵完备等价 | Struct/05-comparative/05.01 |

### 5.2 按文档位置索引

| 文档路径 | 包含定理 | 核心主题 |
|----------|----------|----------|
| `Struct/01-foundation/01.01` | Thm-S-01-01, 01-02 | USTM统一理论 |
| `Struct/01-foundation/01.02` | Thm-S-02-01 | 进程演算基础 |
| `Struct/01-foundation/01.03` | Thm-S-03-01, 03-02 | Actor模型形式化 |
| `Struct/01-foundation/01.04` | Thm-S-04-01 | Dataflow模型 |
| `Struct/01-foundation/01.05` | Thm-S-05-01 | CSP形式化 |
| `Struct/02-properties/02.01` | Thm-S-07-01 | 流计算确定性 |
| `Struct/02-properties/02.02` | Thm-S-08-01, 08-02, 08-03 | 一致性层次 |
| `Struct/02-properties/02.03` | Thm-S-09-01 | Watermark单调性 |
| `Struct/02-properties/02.05` | Thm-S-11-01 | 类型安全推导 |
| `Struct/03-relationships/03.01` | Thm-S-12-01 | Actor→CSP编码 |
| `Struct/03-relationships/03.02` | Thm-S-13-01 | Flink→π演算 |
| `Struct/03-relationships/03.03` | Thm-S-14-01 | 表达能力层次 |
| `Struct/04-proofs/04.01` | Thm-S-17-01 | Checkpoint正确性 |
| `Struct/04-proofs/04.02` | Thm-S-18-01, 18-02 | Exactly-Once正确性 |
| `Struct/04-proofs/04.03` | Thm-S-19-01 | Chandy-Lamport一致性 |
| `Struct/04-proofs/04.05` | Thm-S-21-01 | FG/FGG类型安全 |
| `Struct/04-proofs/04.07` | Thm-S-20-01, 20-02, 23-01 | Choreographic死锁自由 |

### 5.3 按依赖关系索引

#### 依赖Checkpoint一致性的定理

| 定理 | 依赖关系 | 引用位置 |
|------|----------|----------|
| Thm-S-18-01 | Thm-S-17-01 | Lemma-S-18-03证明中 |
| Thm-S-18-03 | Thm-S-17-01 | 状态恢复一致性 |

#### 依赖Chandy-Lamport的定理

| 定理 | 依赖关系 | 引用位置 |
|------|----------|----------|
| Thm-S-17-01 | Thm-S-19-01 | 04.01关系1: Flink Checkpoint ↦ Chandy-Lamport |

---

## 6. 核心定理速查卡

### Thm-S-17-01: Flink Checkpoint一致性定理

```
陈述: Flink的Chandy-Lamport基于Checkpoint算法产生一致全局状态
      Consistent(G_n) ∧ NoOrphans(G_n) ∧ Reachable(G_n)

依赖: Lemma-S-17-01, 17-02, 17-03, 17-04
      Def-S-17-01, 17-02, 17-03, 17-04

应用: Flink Checkpoint机制实现，RocksDB状态后端

位置: Struct/04-proofs/04.01-flink-checkpoint-correctness.md
```

### Thm-S-18-01: Flink Exactly-Once正确性定理

```
陈述: 配置Checkpoint与2PC事务性Sink的Flink作业
      实现端到端Exactly-Once语义
      ∀r ∈ Input. |{e ∈ Output | caused_by(e,r)}| = 1

依赖: Lemma-S-18-01, 18-02, 18-03, 18-04
      Def-S-18-01, 18-02, 18-03, 18-04
      Thm-S-17-01 (Checkpoint一致性)

应用: FlinkKafkaProducer, TwoPhaseCommitSinkFunction

位置: Struct/04-proofs/04.02-flink-exactly-once-correctness.md
```

### Thm-S-19-01: Chandy-Lamport一致性定理

```
陈述: Chandy-Lamport分布式快照算法产生一致全局状态
      Consistent(G) ∧ NoOrphans(G) ∧ Reachable(G)

依赖: Lemma-S-19-01, 19-02, 19-03, 19-04
      Def-S-19-01, 19-02, 19-03, 19-04, 19-05

应用: Flink Checkpoint理论基础，分布式快照算法

位置: Struct/04-proofs/04.03-chandy-lamport-consistency.md
```

### Thm-S-20-01: Choreographic流程序正确性

```
陈述: 良好类型的Choreographic流程序保证通信安全性和死锁自由性

依赖: Def-S-20-01~06
      Lemma-S-20-01, 20-02, 20-03, 20-04

应用: Choral语言，MultiChor扩展，类型驱动流编程

位置: Struct/04-proofs/04.07-deadlock-freedom-choreographic.md
```

---

## 7. 引用参考







---

*文档版本: v1.0 | 创建日期: 2026-04-03 | 状态: 已完成*
*涵盖范围: Struct/ 全部核心定理 (Thm-S-17-01 ~ Thm-S-23-01)*
*总定理数: 31 | 总引理数: 55 | 总定义数: 100*
