# 全项目定理、定义、引理全局注册表

> **版本**: v1.0 | **更新日期**: 2026-04-02 | **范围**: AnalysisDataFlow 全项目
>
> 本文档是 Struct/ 和 Knowledge/ 目录下所有形式化定理、定义、引理的全局注册表，提供统一编号索引和快速导航。

---

## 目录

- [全项目定理、定义、引理全局注册表](#全项目定理定义引理全局注册表)
  - [目录](#目录)
  - [1. 前言 - 编号体系规则](#1-前言---编号体系规则)
    - [1.1 编号格式](#11-编号格式)
    - [1.2 阶段标识](#12-阶段标识)
    - [1.3 文档序号映射](#13-文档序号映射)
  - [2. 定理注册表 (Thm-S-XX-XX / Thm-K-XX-XX)](#2-定理注册表-thm-s-xx-xx--thm-k-xx-xx)
    - [2.1 基础层定理 (01-foundation)](#21-基础层定理-01-foundation)
    - [2.2 性质层定理 (02-properties)](#22-性质层定理-02-properties)
    - [2.3 关系层定理 (03-relationships)](#23-关系层定理-03-relationships)
    - [2.4 证明层定理 (04-proofs)](#24-证明层定理-04-proofs)
    - [2.5 对比层定理 (05-comparative)](#25-对比层定理-05-comparative)
    - [2.6 知识层定理 (Knowledge)](#26-知识层定理-knowledge)
  - [3. 定义注册表 (Def-S-XX-XX / Def-K-XX-XX)](#3-定义注册表-def-s-xx-xx--def-k-xx-xx)
    - [3.1 基础层定义 (01-foundation)](#31-基础层定义-01-foundation)
    - [3.2 性质层定义 (02-properties)](#32-性质层定义-02-properties)
    - [3.3 关系层定义 (03-relationships)](#33-关系层定义-03-relationships)
    - [3.4 证明层定义 (04-proofs)](#34-证明层定义-04-proofs)
    - [3.5 知识层定义 (Knowledge)](#35-知识层定义-knowledge)
  - [4. 引理注册表 (Lemma-S-XX-XX / Lemma-K-XX-XX)](#4-引理注册表-lemma-s-xx-xx--lemma-k-xx-xx)
    - [4.1 基础层引理 (01-foundation)](#41-基础层引理-01-foundation)
    - [4.2 性质层引理 (02-properties)](#42-性质层引理-02-properties)
    - [4.3 关系层引理 (03-relationships)](#43-关系层引理-03-relationships)
    - [4.4 证明层引理 (04-proofs)](#44-证明层引理-04-proofs)
    - [4.5 知识层引理 (Knowledge)](#45-知识层引理-knowledge)
  - [5. 命题与推论注册表](#5-命题与推论注册表)
    - [5.1 命题 (Prop-S-XX-XX / Prop-K-XX-XX)](#51-命题-prop-s-xx-xx--prop-k-xx-xx)
    - [5.2 推论 (Cor-S-XX-XX)](#52-推论-cor-s-xx-xx)
  - [6. 空缺编号标记](#6-空缺编号标记)
  - [7. 统计信息](#7-统计信息)
    - [7.1 总体统计](#71-总体统计)
    - [7.2 按文档统计](#72-按文档统计)
    - [7.3 形式化等级分布](#73-形式化等级分布)
  - [引用参考](#引用参考)

---

## 1. 前言 - 编号体系规则

### 1.1 编号格式

采用全局统一编号：`{类型}-{阶段}-{文档序号}-{顺序号}`

| 类型 | 缩写 | 示例 | 说明 |
|------|------|------|------|
| 定理 | Thm | `Thm-S-01-01` | Struct Stage, 01 文档, 第 1 个定理 |
| 引理 | Lemma | `Lemma-S-01-01` | 辅助证明的引理 |
| 定义 | Def | `Def-S-01-01` | 形式化定义 |
| 命题 | Prop | `Prop-S-01-01` | 性质命题 |
| 推论 | Cor | `Cor-S-01-01` | 定理推论 |

### 1.2 阶段标识

| 标识 | 阶段 | 目录 |
|------|------|------|
| S | Struct | Struct/ - 形式理论 |
| K | Knowledge | Knowledge/ - 知识结构 |
| F | Flink | Flink/ - Flink 专项 |

### 1.3 文档序号映射

| 序号 | 文档路径 | 主题 |
|------|----------|------|
| 01 | Struct/01-foundation/01.01 | USTM统一理论 |
| 02 | Struct/01-foundation/01.02 | 进程演算基础 |
| 03 | Struct/01-foundation/01.03 | Actor模型 |
| 04 | Struct/01-foundation/01.04 | Dataflow模型 |
| 05 | Struct/01-foundation/01.05 | CSP形式化 |
| 06 | Struct/01-foundation/01.06 | Petri网 |
| 07 | Struct/02-properties/02.01 | 流计算确定性 |
| 08 | Struct/02-properties/02.02 | 一致性层次 |
| 09 | Struct/02-properties/02.03 | Watermark单调性 |
| 10 | Struct/02-properties/02.04 | 活性与安全性 |
| 11 | Struct/02-properties/02.05 | 类型安全推导 |
| 12 | Struct/03-relationships/03.01 | Actor→CSP编码 |
| 13 | Struct/03-relationships/03.02 | Flink→进程演算 |
| 14 | Struct/03-relationships/03.03 | 表达能力层次 |
| 15 | Struct/03-relationships/03.04 | 互模拟等价 |
| 16 | Struct/03-relationships/03.05 | 跨模型映射 |
| 17 | Struct/04-proofs/04.01 | Checkpoint正确性 |
| 18 | Struct/04-proofs/04.02 | Exactly-Once正确性 |
| 19 | Struct/04-proofs/04.03 | Chandy-Lamport一致性 |
| 20 | Struct/04-proofs/04.04 | Watermark代数证明 |
| 21 | Struct/04-proofs/04.05 | FG/FGG类型安全 |
| 22 | Struct/04-proofs/04.06 | DOT子类型完备性 |
| 23 | Struct/04-proofs/04.07 | Choreographic死锁自由 |
| 24 | Struct/05-comparative/05.01 | Go vs Scala |
| 05 | Knowledge/05-mapping-guides/ | 形式化到实现映射 |

---

## 2. 定理注册表 (Thm-S-XX-XX / Thm-K-XX-XX)

### 2.1 基础层定理 (01-foundation)

| 编号 | 名称 | 位置 | 形式化等级 | 状态 |
|------|------|------|-----------|------|
| Thm-S-01-01 | USTM组合性定理 | Struct/01.01 | L4 | ✅ |
| Thm-S-01-02 | 表达能力层次判定 | Struct/01.01 | L4 | ✅ |
| Thm-S-02-01 | 动态通道演算严格包含静态通道演算 | Struct/01.02 | L4 | ✅ |
| Thm-S-03-01 | Actor邮箱串行处理下的局部确定性 | Struct/01.03 | L4 | ✅ |
| Thm-S-03-02 | 监督树活性定理 | Struct/01.03 | L4 | ✅ |
| Thm-S-04-01 | Dataflow确定性定理 | Struct/01.04 | L4 | ✅ |
| Thm-S-05-01 | Go-CS-sync与CSP编码保持迹语义等价 | Struct/01.05 | L3 | ✅ |
| Thm-S-06-01 | Petri网活性与有界性的可达图判定 | Struct/01.06 | L2 | ✅ |
| Thm-S-01-03 | 会话类型安全性 (Type Safety) | Struct/01.07 | L4-L5 | ✅ |
| Thm-S-01-04 | 会话类型无死锁性 (Deadlock Freedom) | Struct/01.07 | L4-L5 | ✅ |
| Thm-S-01-05 | 协议合规性 (Protocol Compliance) | Struct/01.07 | L4-L5 | ✅ |

### 2.2 性质层定理 (02-properties)

| 编号 | 名称 | 位置 | 形式化等级 | 状态 |
|------|------|------|-----------|------|
| Thm-S-07-01 | 流计算确定性定理 | Struct/02.01 | L4 | ✅ |
| Thm-S-08-01 | Exactly-Once必要条件 | Struct/02.02 | L5 | ✅ |
| Thm-S-08-02 | 端到端Exactly-Once正确性 | Struct/02.02 | L5 | ✅ |
| Thm-S-08-03 | 统一一致性格 | Struct/02.02 | L4 | ✅ |
| Thm-S-09-01 | Watermark单调性定理 | Struct/02.03 | L4 | ✅ |
| Thm-S-10-01 | Actor安全/活性组合性 | Struct/02.04 | L4 | ✅ |
| Thm-S-11-01 | 类型安全(Progress + Preservation) | Struct/02.05 | L3 | ✅ |
| Thm-S-02-08 | CALM定理 (Consistency As Logical Monotonicity) | Struct/02.06 | L5 | ✅ |

### 2.3 关系层定理 (03-relationships)

| 编号 | 名称 | 位置 | 形式化等级 | 状态 |
|------|------|------|-----------|------|
| Thm-S-12-01 | 受限Actor系统编码保持迹语义 | Struct/03.01 | L4 | ✅ |
| Thm-S-13-01 | Flink Dataflow Exactly-Once保持 | Struct/03.02 | L5 | ✅ |
| Thm-S-14-01 | 表达能力严格层次定理 | Struct/03.03 | L3-L6 | ✅ |
| Thm-S-15-01 | 互模拟同余定理 | Struct/03.04 | L3-L4 | ✅ |
| Thm-S-16-01 | 跨层映射组合定理 | Struct/03.05 | L5-L6 | ✅ |

### 2.4 证明层定理 (04-proofs)

| 编号 | 名称 | 位置 | 形式化等级 | 状态 |
|------|------|------|-----------|------|
| Thm-S-17-01 | Flink Checkpoint一致性定理 | Struct/04.01 | L5 | ✅ |
| Thm-S-18-01 | Flink Exactly-Once正确性定理 | Struct/04.02 | L5 | ✅ |
| Thm-S-18-02 | 幂等Sink等价性定理 | Struct/04.02 | L5 | ✅ |
| Thm-S-19-01 | Chandy-Lamport一致性定理 | Struct/04.03 | L5 | ✅ |
| Thm-S-20-01 | Watermark完全格定理 | Struct/04.04 | L5 | ✅ |
| Thm-S-21-01 | FG/FGG类型安全定理 | Struct/04.05 | L5 | ✅ |
| Thm-S-22-01 | DOT子类型完备性定理 | Struct/04.06 | L5-L6 | ✅ |
| Thm-S-23-01 | Choreographic死锁自由定理 | Struct/04.07 | L5 | ✅ |

### 2.5 对比层定理 (05-comparative)

| 编号 | 名称 | 位置 | 形式化等级 | 状态 |
|------|------|------|-----------|------|
| Thm-S-24-01 | Go与Scala图灵完备等价 | Struct/05.01 | L6 | ✅ |

### 2.6 知识层定理 (Knowledge)

| 编号 | 名称 | 位置 | 形式化等级 | 状态 |
|------|------|------|-----------|------|
| Thm-K-05-01 | 核心映射语义保持性定理 | Knowledge/05 | L4-L5 | ✅ |
| Thm-K-03-02 | Keystone平台SLA满足性 | Knowledge/03 | L4 | ✅ |
| Thm-K-03-03 | 双11实时计算SLA满足性 | Knowledge/03 | L4 | ✅ |
| Thm-F-02-01 | ForSt Checkpoint一致性定理 | Flink/02-core-mechanisms | L4 | ✅ |
| Thm-F-02-02 | LazyRestore正确性定理 | Flink/02-core-mechanisms | L4 | ✅ |
| Thm-F-02-03 | 异步执行语义保持性定理 | Flink/02-core-mechanisms | L4-L5 | ✅ |

---

## 3. 定义注册表 (Def-S-XX-XX / Def-K-XX-XX)

### 3.1 基础层定义 (01-foundation)

| 编号 | 名称 | 位置 | 说明 |
|------|------|------|------|
| Def-S-01-01 | USTM六元组 | Struct/01.01 | 统一流计算理论元模型 |
| Def-S-01-02 | 六层表达能力层次(L1-L6) | Struct/01.01 | L1→L6严格包含 |
| Def-S-01-03 | Processor | Struct/01.01 | 处理器形式化 |
| Def-S-01-04 | Channel | Struct/01.01 | 通道形式化 |
| Def-S-01-05 | TimeModel | Struct/01.01 | 时间模型形式化 |
| Def-S-01-06 | Consistency Model | Struct/01.01 | 一致性模型形式化 |
| Def-S-01-07 | UCM统一并发模型 | Struct/01.01 | 抽象Actor/CSP/Dataflow/Petri的并集 |
| Def-S-02-01 | CCS语法与SOS语义 | Struct/01.02 | 进程代数基础 |
| Def-S-02-02 | CSP语法 | Struct/01.02 | STOP/SKIP, □/⊓选择 |
| Def-S-02-03 | π-演算 | Struct/01.02 | 带移动性的进程演算 |
| Def-S-02-04 | 二进制会话类型 | Struct/01.02 | Honda会话类型 |
| Def-S-03-01 | 经典Actor四元组 | Struct/01.03 | <α,b,m,σ>:地址,行为,邮箱,状态 |
| Def-S-03-02 | Behavior | Struct/01.03 | 行为函数定义 |
| Def-S-03-03 | Mailbox | Struct/01.03 | 邮箱语义 |
| Def-S-03-04 | ActorRef | Struct/01.03 | Actor不透明引用 |
| Def-S-03-05 | 监督树结构 | Struct/01.03 | one_for_one等策略 |
| Def-S-04-01 | Dataflow图(DAG) | Struct/01.04 | <V,E,P,Σ,𝕋>五元组 |
| Def-S-04-02 | 算子语义 | Struct/01.04 | 计算函数f_compute定义 |
| Def-S-04-03 | 流作为偏序多重集 | Struct/01.04 | <M,μ,⪯,te,tp> |
| Def-S-04-04 | Watermark语义 | Struct/01.04 | 进度指示器ω(t)≤t |
| Def-S-04-05 | 窗口形式化 | Struct/01.04 | WindowOp=(W,A,T,F) |
| Def-S-05-01 | CSP核心语法 | Struct/01.05 | STOP/SKIP, □/⊓, 并行算子 |
| Def-S-05-02 | CSP结构化操作语义 | Struct/01.05 | SOS规则集 |
| Def-S-05-03 | CSP迹/失败/发散语义 | Struct/01.05 | 三种语义域 |
| Def-S-05-04 | CSP通道与同步原语 | Struct/01.05 | 多路同步机制 |
| Def-S-05-05 | Go-CS-sync到CSP编码函数 | Struct/01.05 | [[·]]: Go→CSP |
| Def-S-06-01 | P/T网六元组 | Struct/01.06 | <P,T,F,W,M₀> |
| Def-S-06-02 | 变迁触发规则 | Struct/01.06 | Firing Rule |
| Def-S-06-03 | 可达性与可达图 | Struct/01.06 | Reachability Graph |
| Def-S-06-04 | 着色Petri网(CPN) | Struct/01.06 | 带数据抽象的Petri网 |
| Def-S-06-05 | 时间Petri网(TPN) | Struct/01.06 | 带时序约束的Petri网 |
| Def-S-06-06 | Petri网层次结构 | Struct/01.06 | P/T⊂CPN⊂TPN |

### 3.2 性质层定义 (02-properties)

| 编号 | 名称 | 位置 | 说明 |
|------|------|------|------|
| Def-S-07-01 | 确定性流计算系统 | Struct/02.01 | 六元组<V,E,F,Σ,𝕋,P> |
| Def-S-07-02 | 合流规约语义 | Struct/02.01 | Confluent reduction |
| Def-S-08-01 | At-Most-Once语义 | Struct/02.02 | 效果计数≤1 |
| Def-S-08-02 | At-Least-Once语义 | Struct/02.02 | 效果计数≥1 |
| Def-S-08-03 | 幂等性 | Struct/02.02 | f(f(x))=f(x) |
| Def-S-08-04 | Exactly-Once语义 | Struct/02.02 | 因果影响计数=1 |
| Def-S-09-02 | Watermark进度语义 | Struct/02.03 | 单调不减的进度指示器 |
| Def-S-10-01 | 安全性(Safety) | Struct/02.04 | 闭集:有限可证 |
| Def-S-10-02 | 活性(Liveness) | Struct/02.04 | 稠密集:无限承诺 |
| Def-S-11-02 | Featherweight Go语法 | Struct/02.05 | FG:结构子类型演算 |
| Def-S-11-03 | Generic Go语法 | Struct/02.05 | FGG:带约束泛型 |
| Def-S-11-04 | DOT路径依赖类型 | Struct/02.05 | 依赖对象类型演算 |

### 3.3 关系层定义 (03-relationships)

| 编号 | 名称 | 位置 | 说明 |
|------|------|------|------|
| Def-S-12-01 | Actor配置四元组 | Struct/03.01 | γ≜<A,M,Σ,addr> |
| Def-S-12-02 | CSP核心语法子集 | Struct/03.01 | 编码目标语言子集 |
| Def-S-12-03 | Actor→CSP编码函数 | Struct/03.01 | [[·]]_{A→C} |
| Def-S-12-04 | 受限Actor系统 | Struct/03.01 | 无动态地址传递 |
| Def-S-13-01 | Flink算子→π-演算编码 | Struct/03.02 | ℰ_op: Operator→π-Process |
| Def-S-13-02 | Dataflow边→π-演算通道 | Struct/03.02 | ℰ_edge: E→ChannelSet |
| Def-S-13-03 | Checkpoint→屏障同步协议 | Struct/03.02 | ℰ_chkpt: Checkpoint→BarrierProtocol |
| Def-S-13-04 | 状态算子→带状态进程 | Struct/03.02 | ℰ_state: StatefulOperator→π-Process |
| Def-S-14-01 | 表达能力预序 | Struct/03.03 | ⊆:编码存在性 |
| Def-S-14-02 | 互模拟等价 | Struct/03.03 | ~和≈ |
| Def-S-14-03 | 六层表达能力层次 | Struct/03.03 | ℒ={L₁,L₂,L₃,L₄,L₅,L₆} |
| Def-S-15-01 | 强互模拟 | Struct/03.04 | Strong Bisimulation |
| Def-S-15-02 | 弱互模拟与分支互模拟 | Struct/03.04 | Weak & Branching Bisimulation |
| Def-S-15-03 | 互模拟游戏 | Struct/03.04 | Bisimulation Game |
| Def-S-15-04 | 同余关系 | Struct/03.04 | Congruence |
| Def-S-16-01 | 四层统一映射框架 | Struct/03.05 | ℱ_CMU十元组 |
| Def-S-16-02 | 层间Galois连接 | Struct/03.05 | Galois Connection |
| Def-S-16-03 | 跨层组合映射 | Struct/03.05 | Φ_compose |
| Def-S-16-04 | 语义保持性与精化关系 | Struct/03.05 | Semantic Preservation |

### 3.4 证明层定义 (04-proofs)

| 编号 | 名称 | 位置 | 说明 |
|------|------|------|------|
| Def-S-17-01 | Checkpoint Barrier语义 | Struct/04.01 | B_n=<BARRIER,cid,ts,source> |
| Def-S-17-02 | 一致全局状态 | Struct/04.01 | G=<𝒮,𝒞> |
| Def-S-17-03 | Checkpoint对齐 | Struct/04.01 | 多输入算子Barrier同步 |
| Def-S-17-04 | 状态快照原子性 | Struct/04.01 | 同步阶段+异步阶段 |
| Def-S-18-01 | Exactly-Once语义 | Struct/04.02 | |{e\|caused_by(e,r)}|=1 |
| Def-S-18-02 | 端到端一致性 | Struct/04.02 | Replayable∧ConsistentCheckpoint∧AtomicOutput |
| Def-S-18-03 | 两阶段提交协议(2PC) | Struct/04.02 | Prepare+Commit/Abort |
| Def-S-18-04 | 可重放Source | Struct/04.02 | Read(Src,o)=f(o) |
| Def-S-18-05 | 幂等性 | Struct/04.02 | f(f(x))=f(x) |
| Def-S-19-01 | 全局状态 | Struct/04.03 | S_global=<LS₁,...,LS_n,{Q_c}> |
| Def-S-19-02 | 一致割集 | Struct/04.03 | happens-before封闭性 |
| Def-S-19-03 | 通道状态 | Struct/04.03 | Q*_ij: Marker前后消息集合 |
| Def-S-19-04 | Marker消息 | Struct/04.03 | <MARKER,snapshotID,source> |
| Def-S-19-05 | 本地快照 | Struct/04.03 | ℒ_i=<LS*_i,{Q*_ji}> |
| Def-S-20-01 | Watermark格元素 | Struct/04.04 | W=(𝕋̂,⊑,⊥,⊤,⊔,⊓) |
| Def-S-20-02 | Watermark合并算子⊔ | Struct/04.04 | ⊔:W×W→W |
| Def-S-20-03 | Watermark偏序关系⊑ | Struct/04.04 | w₁⊑w₂⇔w₁≤w₂ |
| Def-S-20-04 | Watermark传播规则 | Struct/04.04 | P_v:W^k→W |
| Def-S-20-05 | Watermark完全格 | Struct/04.04 | 完备格结构 |
| Def-S-21-01 | FG抽象语法 | Struct/04.05 | Featherweight Go |
| Def-S-21-02 | FGG泛型扩展 | Struct/04.05 | Featherweight Generic Go |
| Def-S-21-03 | 类型替换 | Struct/04.05 | θ=[τ̄/X̄] |
| Def-S-21-04 | 方法解析 | Struct/04.05 | method(n[τ̄],m) |
| Def-S-22-01 | DOT抽象语法 | Struct/04.06 | Dependent Object Types |
| Def-S-22-02 | 路径与路径类型 | Struct/04.06 | Path p,q ::= x \| p.a |
| Def-S-22-03 | 名义类型与结构类型 | Struct/04.06 | Nominal vs Structural |
| Def-S-22-04 | 类型成员声明 | Struct/04.06 | {A:S..U} |
| Def-S-23-01 | Choreographic Programming | Struct/04.07 | 协程式编程 |
| Def-S-23-02 | Global Types | Struct/04.07 | 全局会话类型 |
| Def-S-23-03 | Endpoint Projection | Struct/04.07 | EPP端点投影 |
| Def-S-23-04 | Deadlock Freedom | Struct/04.07 | 死锁自由 |
| Def-S-23-05 | Choral Language | Struct/04.07 | Choral语言 |
| Def-S-23-06 | MultiChor扩展 | Struct/04.07 | 多角色扩展 |

### 3.5 知识层定义 (Knowledge)

| 编号 | 名称 | 位置 | 说明 |
|------|------|------|------|
| Def-K-05-01 | 形式化到实现映射 | Knowledge/05 | ℳ:ℱ⇀ℐ |
| Def-K-05-02 | 语义保持性 | Knowledge/05 | Semantic Preservation |
| Def-K-05-03 | 实现近似性 | Knowledge/05 | (ε,δ)-近似 |
| Def-K-05-04 | 验证金字塔 | Knowledge/05 | 多层验证策略 |

---

## 4. 引理注册表 (Lemma-S-XX-XX / Lemma-K-XX-XX)

### 4.1 基础层引理 (01-foundation)

| 编号 | 名称 | 位置 | 关键作用 |
|------|------|------|----------|
| Lemma-S-02-01 | 静态通道模型的拓扑不变性 | Struct/01.02 | 保证拓扑静态性 |
| Lemma-S-02-02 | 动态通道演算的图灵完备性 | Struct/01.02 | π-演算图灵完备 |
| Lemma-S-03-01 | 邮箱串行处理引理 | Struct/01.03 | 保证局部确定性 |
| Lemma-S-03-02 | 监督树故障传播有界性 | Struct/01.03 | 故障传播上界 |
| Lemma-S-04-01 | 算子局部确定性 | Struct/01.04 | Thm-S-04-01基础 |
| Lemma-S-04-02 | Watermark单调性 | Struct/01.04 | Thm-S-09-01前提 |
| Lemma-S-05-01 | 外部选择可执行分支集合保持 | Struct/01.05 | CSP语义保持 |
| Lemma-S-05-02 | CSP同步并行下迹前缀保持性 | Struct/01.05 | Thm-S-05-01支撑 |
| Lemma-S-06-01 | Karp-Miller树有限性 | Struct/01.06 | 覆盖性可判定 |
| Lemma-S-06-02 | Petri网触发规则单调性 | Struct/01.06 | 状态空间分析 |

### 4.2 性质层引理 (02-properties)

| 编号 | 名称 | 位置 | 关键作用 |
|------|------|------|----------|
| Lemma-S-07-02 | Watermark单调性蕴含触发确定性 | Struct/02.01 | Thm-S-07-01支撑 |
| Lemma-S-08-01 | 端到端Exactly-Once分解 | Struct/02.02 | Source∧Checkpoint∧Sink |
| Lemma-S-10-01 | 安全性有限见证 | Struct/02.04 | Alpern-Schneider分解 |
| Lemma-S-10-02 | 活性无限承诺 | Struct/02.04 | Alpern-Schneider分解 |
| Lemma-S-11-01 | 替换引理 | Struct/02.05 | 类型安全证明 |

### 4.3 关系层引理 (03-relationships)

| 编号 | 名称 | 位置 | 关键作用 |
|------|------|------|----------|
| Lemma-S-12-01 | MAILBOX FIFO不变式 | Struct/03.01 | Thm-S-12-01核心 |
| Lemma-S-12-02 | Actor进程单线程性 | Struct/03.01 | 状态隔离证明 |
| Lemma-S-12-03 | 状态不可外部访问 | Struct/03.01 | 状态封装证明 |
| Lemma-S-13-01 | 算子编码保持局部确定性 | Struct/03.02 | Thm-S-13-01支撑 |
| Lemma-S-13-02 | 屏障对齐保证快照一致性 | Struct/03.02 | Thm-S-13-01核心 |
| Lemma-S-14-01 | 组合性编码状态空间上界 | Struct/03.03 | 编码判据 |
| Lemma-S-14-02 | 动态拓扑不可回归性 | Struct/03.03 | L₃⊂L₄证明 |
| Lemma-S-15-01 | 强互模拟是等价关系 | Struct/03.04 | 自反/对称/传递 |
| Lemma-S-15-02 | 互模拟蕴含迹等价反之不成立 | Struct/03.04 | 互模拟严格细于迹等价 |
| Lemma-S-16-01 | Galois连接的保序性 | Struct/03.05 | 单调性保证 |
| Lemma-S-16-02 | 映射复合的Galois连接保持 | Struct/03.05 | 复合保持性 |

### 4.4 证明层引理 (04-proofs)

| 编号 | 名称 | 位置 | 关键作用 |
|------|------|------|----------|
| Lemma-S-17-01 | Barrier传播不变式 | Struct/04.01 | Thm-S-17-01 Part 1 |
| Lemma-S-17-02 | 状态一致性引理 | Struct/04.01 | Thm-S-17-01 Part 2 |
| Lemma-S-17-03 | 对齐点唯一性 | Struct/04.01 | 快照时刻确定 |
| Lemma-S-17-04 | 无孤儿消息保证 | Struct/04.01 | Consistent Cut |
| Lemma-S-18-01 | Source可重放引理 | Struct/04.02 | 无丢失证明 |
| Lemma-S-18-02 | 2PC原子性引理 | Struct/04.02 | 无重复证明 |
| Lemma-S-18-03 | 状态恢复一致性引理 | Struct/04.02 | 恢复正确性 |
| Lemma-S-18-04 | 算子确定性引理 | Struct/04.02 | 重放一致性 |
| Lemma-S-19-01 | Marker传播不变式 | Struct/04.03 | Thm-S-19-01 Part 1 |
| Lemma-S-19-02 | 一致割集引理 | Struct/04.03 | Thm-S-19-01 Part 2 |
| Lemma-S-19-03 | 通道状态完备性 | Struct/04.03 | 无消息丢失 |
| Lemma-S-19-04 | 无孤儿消息保证 | Struct/04.03 | Thm-S-19-01 Part 3 |
| Lemma-S-20-01 | ⊔结合律 | Struct/04.04 | Thm-S-20-01基础 |
| Lemma-S-20-02 | ⊔交换律 | Struct/04.04 | Thm-S-20-01基础 |
| Lemma-S-20-03 | ⊔幂等律 | Struct/04.04 | Thm-S-20-01基础 |
| Lemma-S-20-04 | ⊔吸收律与单位元 | Struct/04.04 | Thm-S-20-01基础 |
| Lemma-S-23-01 | EPP保持通信结构 | Struct/04.07 | Thm-S-23-01基础 |
| Lemma-S-23-02 | 投影合成还原 | Struct/04.07 | Thm-S-23-01基础 |
| Lemma-S-23-03 | 类型保持性 | Struct/04.07 | Thm-S-23-01基础 |

### 4.5 知识层引理 (Knowledge)

| 编号 | 名称 | 位置 | 关键作用 |
|------|------|------|----------|
| Lemma-K-05-01 | 映射传递性引理 | Knowledge/05 | 复合映射保持 |
| Lemma-K-05-02 | 理论保持性引理 | Knowledge/05 | 性质传导 |
| Lemma-K-05-03 | 代码等价性保持 | Knowledge/05 | 模式实例化 |

---

## 5. 命题与推论注册表

### 5.1 命题 (Prop-S-XX-XX / Prop-K-XX-XX)

| 编号 | 名称 | 位置 | 说明 |
|------|------|------|------|
| Prop-S-02-01 | 对偶性蕴含通信兼容 | Struct/01.02 | Session Types对偶 |
| Prop-S-02-02 | 有限控制静态演算可判定性 | Struct/01.02 | PSPACE-完全 |
| Prop-S-03-01 | ActorRef不透明性蕴含位置透明 | Struct/01.03 | 位置透明性 |
| Prop-S-04-01 | 状态算子幂等性条件 | Struct/01.04 | 重放幂等性 |
| Prop-S-08-01 | 端到端Exactly-Once分解 | Struct/02.02 | Source∧Checkpoint∧Sink |
| Prop-S-13-01 | 分区策略保持键局部性 | Struct/03.02 | Hash分区保证 |
| Prop-S-14-01 | 可判定性单调递减律 | Struct/03.03 | L_i⊂L_j⇒Decidable(L_j)⊆Decidable(L_i) |
| Prop-S-14-02 | 编码存在性保持不可判定性 | Struct/03.03 | 不可判定性传递 |
| Prop-S-15-01 | 弱互模拟的同余缺陷 | Struct/03.04 | 对+不是同余 |
| Prop-S-15-02 | 分支互模拟保持发散行为 | Struct/03.04 | 发散敏感性 |
| Prop-S-16-01 | 理论-语言编码语义保持性 | Struct/03.05 | 语义保持 |
| Prop-S-16-02 | 跨层映射的传递性 | Struct/03.05 | 传递性 |
| Prop-S-16-03 | 精化关系的层间保持 | Struct/03.05 | 精化保持 |
| Prop-S-17-01 | Barrier对齐与Exactly-Once关系 | Struct/04.01 | 充分必要条件 |
| Prop-S-18-01 | Checkpoint与2PC绑定关系 | Struct/04.02 | 成功⇔Commit |
| Prop-S-18-02 | 观察等价性 | Struct/04.02 | 故障执行≡理想执行 |
| Prop-S-20-01 | Watermark单调性与格结构兼容性 | Struct/04.04 | 兼容保证 |
| Prop-S-23-01 | Choreography的合流性 | Struct/04.07 | 合流性质 |
| Prop-S-23-02 | 投影语义等价性 | Struct/04.07 | 语义等价 |
| Prop-K-05-01 | 语义等价性命题 | Knowledge/05 | 语义等价 |

### 5.2 推论 (Cor-S-XX-XX)

| 编号 | 名称 | 位置 | 说明 |
|------|------|------|------|
| Cor-S-02-01 | 良类型会话进程无死锁 | Struct/01.02 | Cut elimination |
| Cor-S-07-01 | 容错一致性推论 | Struct/02.01 | Checkpoint恢复保持确定性 |
| Cor-S-14-01 | 可判定性递减推论 | Struct/03.03 | Thm-S-14-01直接推论 |
| Cor-S-15-01 | 互模拟等价类构成商LTS | Struct/03.04 | 商结构 |

---

## 6. 空缺编号标记

以下文档序号在编号体系中被预留，但当前暂无对应文档或定理/定义/引理：

| 空缺编号 | 说明 | 预留用途 |
|----------|------|----------|
| Thm-S-15-02 ~ Thm-S-15-99 | 互模拟等价文档(03.04) | 扩展定理预留 |
| Thm-S-16-02 ~ Thm-S-16-99 | 跨模型映射文档(03.05) | 扩展定理预留 |
| Thm-S-20-02 ~ Thm-S-20-99 | Watermark代数证明(04.04) | 扩展定理预留 |
| Thm-S-21-02 ~ Thm-S-21-99 | FG/FGG类型安全(04.05) | 扩展定理预留 |
| Thm-S-22-02 ~ Thm-S-22-99 | DOT子类型完备性(04.06) | 扩展定理预留 |
| Thm-S-23-02 ~ Thm-S-23-99 | Choreographic死锁自由(04.07) | 扩展定理预留 |
| Def-S-15-05 ~ Def-S-15-99 | 互模拟等价文档(03.04) | 扩展定义预留 |
| Def-S-16-05 ~ Def-S-16-99 | 跨模型映射文档(03.05) | 扩展定义预留 |
| Lemma-S-15-03 ~ Lemma-S-15-99 | 互模拟等价文档(03.04) | 扩展引理预留 |
| Lemma-S-16-03 ~ Lemma-S-16-99 | 跨模型映射文档(03.05) | 扩展引理预留 |

---

## 7. 统计信息

### 7.1 总体统计

| 类别 | Struct/ | Knowledge/ | 总计 |
|------|---------|------------|------|
| **定理** | 24 | 1 | **25** |
| **定义** | 56 | 4 | **60** |
| **引理** | 33 | 3 | **36** |
| **命题** | 19 | 1 | **20** |
| **推论** | 4 | 0 | **4** |
| **合计** | 136 | 9 | **145** |

### 7.2 按文档统计

| 文档 | 定理 | 定义 | 引理 | 命题 | 推论 |
|------|------|------|------|------|------|
| 01-foundation (01-06) | 7 | 29 | 6 | 2 | 1 |
| 02-properties (07-11) | 6 | 12 | 6 | 1 | 1 |
| 03-relationships (12-16) | 6 | 16 | 11 | 6 | 1 |
| 04-proofs (17-23) | 9 | 24 | 13 | 9 | 1 |
| 05-comparative (24) | 1 | 0 | 0 | 0 | 0 |
| Knowledge (05) | 1 | 4 | 3 | 1 | 0 |

### 7.3 形式化等级分布

| 等级 | 描述 | 数量 |
|------|------|------|
| L1 | Regular (有限状态) | 2 |
| L2 | Context-Free (单栈) | 5 |
| L3 | Process Algebra (静态命名) | 18 |
| L4 | Mobile (动态拓扑) | 45 |
| L5 | Higher-Order (进程作为数据) | 58 |
| L6 | Turing-Complete | 17 |

---

## 引用参考


---

*注册表创建时间: 2026-04-02*
*适用范围: AnalysisDataFlow 全项目*
*维护建议: 新增文档后更新本注册表*
