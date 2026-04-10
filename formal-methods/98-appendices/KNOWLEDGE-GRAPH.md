# 形式化方法知识图谱 (Knowledge Graph)

> **所属**: formal-methods/98-appendices
>
> **定位**: 全局知识网络，连接所有核心概念与文档
>
> **版本**: v1.0 | **更新日期**: 2026-04-10

---

## 🌐 全局概念关系图

```mermaid
graph TB
    subgraph "数学基础层"
        ST[集合论<br/>Set Theory]
        CT[范畴论<br/>Category Theory]
        DT[域论<br/>Domain Theory]
        OT[序理论<br/>Order Theory]
    end
    
    subgraph "逻辑层"
        FOL[一阶逻辑<br/>First-Order Logic]
        ML[模态逻辑<br/>Modal Logic]
        TL[时序逻辑<br/>Temporal Logic]
        HL[霍尔逻辑<br/>Hoare Logic]
    end
    
    subgraph "类型与计算"
        TT[类型论<br/>Type Theory]
        LC[λ演算<br/>Lambda Calculus]
        AI[抽象解释<br/>Abstract Interpretation]
    end
    
    subgraph "并发模型"
        PC[进程演算<br/>Process Calculus]
        BS[互模拟<br/>Bisimulation]
        PN[Petri网<br/>Petri Nets]
    end
    
    subgraph "验证技术"
        MC[模型检测<br/>Model Checking]
        TP[定理证明<br/>Theorem Proving]
        FM[形式化方法<br/>Formal Methods]
    end
    
    subgraph "分布式系统"
        DC[分布式计算<br/>Distributed Computing]
        CON[共识<br/>Consensus]
        BFT[拜占庭容错<br/>Byzantine Fault Tolerance]
        CAP[CAP定理<br/>CAP Theorem]
        LIN[线性一致性<br/>Linearizability]
        SER[可串行化<br/>Serializability]
    end
    
    subgraph "分布式算法"
        PAX[Paxos]
        RAFT[Raft]
        TPC[2PC/3PC]
        DHT[DHT]
    end
    
    %% 数学基础到逻辑
    ST --> FOL
    CT --> ML
    DT --> TT
    OT --> DT
    
    %% 逻辑到类型/计算
    FOL --> TT
    ML --> TL
    FOL --> HL
    
    %% 类型到并发
    TT --> LC
    LC --> PC
    TT --> AI
    
    %% 并发模型间
    PC --> BS
    PC --> PN
    BS --> MC
    
    %% 验证技术
    MC --> FM
    TP --> FM
    TL --> MC
    HL --> TP
    AI --> MC
    
    %% 到分布式系统
    FM --> DC
    DC --> CON
    CON --> BFT
    DC --> CAP
    CAP --> LIN
    CAP --> SER
    
    %% 到具体算法
    CON --> PAX
    CON --> RAFT
    CON --> TPC
    DC --> DHT
    
    %% 一致性
    LIN --> PAX
    LIN --> RAFT
    SER --> TPC
```

---

## 📚 文档依赖关系图

```mermaid
graph BT
    subgraph "基础层"
        F01[01-foundations/<br/>order-theory]
        F02[01-foundations/<br/>category-theory]
        F03[01-foundations/<br/>logic-foundations]
        F04[01-foundations/<br/>domain-theory]
        F05[01-foundations/<br/>type-theory]
    end
    
    subgraph "演算层"
        C01[02-calculi/<br/>w-calculus-family]
        C02[02-calculi/<br/>pi-calculus]
        C03[02-calculi/<br/>stream-calculus]
    end
    
    subgraph "模型层"
        M01[03-model-taxonomy/<br/>system-models]
        M02[03-model-taxonomy/<br/>computation-models]
        M03[03-model-taxonomy/<br/>consistency]
    end
    
    subgraph "应用层"
        A01[04-application-layer/<br/>workflow]
        A02[04-application-layer/<br/>stream-processing]
        A03[04-application-layer/<br/>cloud-native]
    end
    
    subgraph "验证层"
        V01[05-verification/<br/>logic]
        V02[05-verification/<br/>model-checking]
        V03[05-verification/<br/>theorem-proving]
    end
    
    subgraph "工具层"
        T01[06-tools/<br/>academic]
        T02[06-tools/<br/>industrial]
    end
    
    subgraph "AI层"
        AI01[08-ai-formal-methods/<br/>neural-theorem-proving]
        AI02[08-ai-formal-methods/<br/>llm-formalization]
        AI03[08-ai-formal-methods/<br/>nn-verification]
    end
    
    subgraph "概念层"
        W01[wikipedia-concepts/<br/>all-25-concepts]
    end
    
    %% 依赖关系
    F01 --> F04
    F02 --> F05
    F03 --> V01
    F04 --> C03
    F05 --> V03
    
    F03 --> C02
    F05 --> C02
    
    C01 --> C03
    C02 --> M02
    C03 --> A02
    
    M01 --> M03
    M02 --> V02
    M03 --> A03
    
    V01 --> V02
    V01 --> V03
    V02 --> T01
    V03 --> T01
    
    A03 --> T02
    
    V03 --> AI01
    FM --> AI02
    V02 --> AI03
    
    %% 所有层到概念层
    F01 --> W01
    F02 --> W01
    C02 --> W01
    M03 --> W01
    V01 --> W01
    T02 --> W01
```

---

## 🎯 学习路径图

```mermaid
graph LR
    subgraph "入门路径"
        START[开始]
        FM[形式化方法<br/>概念]
        LOGIC[逻辑基础]
    end
    
    subgraph "基础路径"
        TYPES[类型论]
        LAMBDA[λ演算]
        PI[π演算]
    end
    
    subgraph "验证路径"
        MC[模型检测]
        TP[定理证明]
        AI[抽象解释]
    end
    
    subgraph "分布式路径"
        CONS[共识理论]
        PAXOS[Paxos/Raft]
        CAP[CAP定理]
    end
    
    subgraph "高级路径"
        HOTT[同伦类型论]
    end
    
    START --> FM
    FM --> LOGIC
    
    LOGIC --> TYPES
    TYPES --> LAMBDA
    LAMBDA --> PI
    
    PI --> MC
    TYPES --> TP
    LAMBDA --> AI
    
    MC --> CONS
    TP --> CONS
    CONS --> PAXOS
    CONS --> CAP
    
    TP --> HOTT
    TYPES --> HOTT
```

---

## 🔬 概念深度页导航

### 按类别导航

#### 形式化方法基础 (10个)
```mermaid
mindmap
  root((形式化方法<br/>基础))
    规约
      Formal Methods
      Process Calculus
    验证
      Model Checking
      Theorem Proving
      Abstract Interpretation
    逻辑
      Temporal Logic
      Hoare Logic
    并发
      Bisimulation
      Petri Nets
    类型
      Type Theory
```

#### 分布式系统核心 (10个)
```mermaid
mindmap
  root((分布式系统<br/>核心))
    基础
      Distributed Computing
    一致性
      Consensus
      CAP Theorem
      Linearizability
      Serializability
    容错
      Byzantine Fault Tolerance
    算法
      Paxos
      Raft
      Two Phase Commit
      Distributed Hash Table
```

#### 逻辑与数学基础 (5个)
```mermaid
mindmap
  root((逻辑与数学<br/>基础))
    逻辑
      Modal Logic
      First Order Logic
    数学
      Set Theory
      Domain Theory
      Category Theory
```

---

## 📊 统计信息

| 指标 | 数值 |
|------|------|
| **核心概念总数** | 25 |
| **文档总数** | 81+ |
| **形式化定义** | 350+ |
| **定理/引理** | 200+ |
| **证明数量** | 100+ |
| **Mermaid图表** | 300+ |
| **引用文献** | 200+ |

---

## 🔗 快速链接

### Wikipedia核心概念深度页
- [形式化方法](wikipedia-concepts/01-formal-methods.md)
- [模型检测](wikipedia-concepts/02-model-checking.md)
- [定理证明](wikipedia-concepts/03-theorem-proving.md)
- [进程演算](wikipedia-concepts/04-process-calculus.md)
- [时序逻辑](wikipedia-concepts/05-temporal-logic.md)
- [霍尔逻辑](wikipedia-concepts/06-hoare-logic.md)
- [类型论](wikipedia-concepts/07-type-theory.md)
- [抽象解释](wikipedia-concepts/08-abstract-interpretation.md)
- [互模拟](wikipedia-concepts/09-bisimulation.md)
- [Petri网](wikipedia-concepts/10-petri-nets.md)
- [分布式计算](wikipedia-concepts/11-distributed-computing.md)
- [拜占庭容错](wikipedia-concepts/12-byzantine-fault-tolerance.md)
- [共识](wikipedia-concepts/13-consensus.md)
- [CAP定理](wikipedia-concepts/14-cap-theorem.md)
- [线性一致性](wikipedia-concepts/15-linearizability.md)
- [可串行化](wikipedia-concepts/16-serializability.md)
- [两阶段提交](wikipedia-concepts/17-two-phase-commit.md)
- [Paxos](wikipedia-concepts/18-paxos.md)
- [Raft](wikipedia-concepts/19-raft.md)
- [分布式哈希表](wikipedia-concepts/20-distributed-hash-table.md)
- [模态逻辑](wikipedia-concepts/21-modal-logic.md)
- [一阶逻辑](wikipedia-concepts/22-first-order-logic.md)
- [集合论](wikipedia-concepts/23-set-theory.md)
- [域论](wikipedia-concepts/24-domain-theory.md)
- [范畴论](wikipedia-concepts/25-category-theory.md)

---

## 📝 维护信息

- **创建日期**: 2026-04-10
- **最后更新**: 2026-04-10
- **维护者**: 形式化方法文档组
- **贡献指南**: 欢迎提交PR补充新的概念关系
