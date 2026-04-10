# 分布式系统形式化计算模型全景图谱

---

## 目录

- [分布式系统形式化计算模型全景图谱](#分布式系统形式化计算模型全景图谱)
  - [目录](#目录)
  - [一、经典模型](#一经典模型)
    - [1.1 状态机模型](#11-状态机模型)
      - [1.1.1 有限状态机（FSM）](#111-有限状态机fsm)
      - [1.1.2 扩展状态机](#112-扩展状态机)
    - [1.2 Petri网](#12-petri网)
      - [1.2.1 基本Petri网](#121-基本petri网)
      - [1.2.2 有色Petri网（CPN）](#122-有色petri网cpn)
      - [1.2.3 时序Petri网](#123-时序petri网)
    - [1.3 进程代数](#13-进程代数)
      - [1.3.1 CSP（通信顺序进程）](#131-csp通信顺序进程)
      - [1.3.2 CCS（通信系统演算）](#132-ccs通信系统演算)
      - [1.3.3 π演算](#133-π演算)
  - [二、工作流模型](#二工作流模型)
    - [2.1 BPMN语义基础](#21-bpmn语义基础)
      - [2.1.1 BPMN核心元素形式化](#211-bpmn核心元素形式化)
    - [2.2 工作流网（WF-nets）](#22-工作流网wf-nets)
      - [2.2.1 形式化定义](#221-形式化定义)
    - [2.3 YAWL（Yet Another Workflow Language）](#23-yawlyet-another-workflow-language)
      - [2.3.1 形式化定义](#231-形式化定义)
    - [2.4 BPEL形式化](#24-bpel形式化)
      - [2.4.1 BPEL核心结构形式化](#241-bpel核心结构形式化)
  - [三、流计算模型](#三流计算模型)
    - [3.1 数据流模型](#31-数据流模型)
      - [3.1.1 Kahn进程网络（KPN）](#311-kahn进程网络kpn)
      - [3.1.2 同步数据流（SDF）](#312-同步数据流sdf)
    - [3.2 复杂事件处理（CEP）](#32-复杂事件处理cep)
      - [3.2.1 事件代数](#321-事件代数)
      - [3.2.2 事件模式形式化](#322-事件模式形式化)
    - [3.3 流处理系统形式化基础](#33-流处理系统形式化基础)
      - [3.3.1 流处理算子代数](#331-流处理算子代数)
      - [3.3.2 一致性模型](#332-一致性模型)
  - [四、云原生模型](#四云原生模型)
    - [4.1 容器编排形式化](#41-容器编排形式化)
      - [4.1.1 Kubernetes调度理论](#411-kubernetes调度理论)
      - [4.1.2 声明式配置语义](#412-声明式配置语义)
    - [4.2 微服务交互模型](#42-微服务交互模型)
      - [4.2.1 服务调用模式](#421-服务调用模式)
    - [4.3 服务网格通信模型](#43-服务网格通信模型)
      - [4.3.1 Sidecar代理模型](#431-sidecar代理模型)
    - [4.4 无服务器计算模型](#44-无服务器计算模型)
      - [4.4.1 函数即服务形式化](#441-函数即服务形式化)
  - [五、新兴模型](#五新兴模型)
    - [5.1 Actor模型](#51-actor模型)
      - [5.1.1 基本Actor模型](#511-基本actor模型)
      - [5.1.2 扩展Actor模型](#512-扩展actor模型)
    - [5.2 CRDT理论](#52-crdt理论)
      - [5.2.1 形式化定义](#521-形式化定义)
      - [5.2.2 CRDT类型](#522-crdt类型)
    - [5.3 共识算法形式化](#53-共识算法形式化)
      - [5.3.1 共识问题定义](#531-共识问题定义)
      - [5.3.2 Paxos形式化](#532-paxos形式化)
      - [5.3.3 Raft形式化](#533-raft形式化)
    - [5.4 区块链形式化模型](#54-区块链形式化模型)
      - [5.4.1 区块链抽象模型](#541-区块链抽象模型)
      - [5.4.2 共识机制形式化](#542-共识机制形式化)
      - [5.4.3 智能合约形式化](#543-智能合约形式化)
  - [六、模型对比与总结](#六模型对比与总结)
    - [6.1 表达能力层次](#61-表达能力层次)
    - [6.2 模型综合对比表](#62-模型综合对比表)
    - [6.3 模型选择决策树](#63-模型选择决策树)
    - [6.4 模型演进趋势](#64-模型演进趋势)
  - [附录：数学符号表](#附录数学符号表)

---

## 一、经典模型

### 1.1 状态机模型

#### 1.1.1 有限状态机（FSM）

**形式化定义**

有限状态机是一个五元组 $M = (Q, \Sigma, \delta, q_0, F)$，其中：

- $Q$：有限状态集合
- $\Sigma$：有限输入字母表
- $\delta: Q \times \Sigma \rightarrow Q$：状态转移函数
- $q_0 \in Q$：初始状态
- $F \subseteq Q$：接受状态集合

**扩展：Mealy机与Moore机**

**Mealy机**：输出依赖于当前状态和输入
$$M_{Mealy} = (Q, \Sigma, \Gamma, \delta, \lambda, q_0)$$
其中 $\lambda: Q \times \Sigma \rightarrow \Gamma$ 为输出函数

**Moore机**：输出仅依赖于当前状态
$$M_{Moore} = (Q, \Sigma, \Gamma, \delta, \lambda, q_0)$$
其中 $\lambda: Q \rightarrow \Gamma$ 为输出函数

**表达能力分析**

| 特性 | 表达能力 | 复杂度 |
|------|----------|--------|
| 正则语言识别 | 完全 | $O(n)$ 状态数 |
| 非确定性FSM | 等价于DFSM | 状态数指数级增长 |
| 表达能力层级 | 正则语言 $\subset$ 上下文无关语言 | - |

**典型应用场景**

- 协议状态管理（TCP连接状态）
- UI状态管理（Redux、Vuex）
- 编译器词法分析
- 游戏AI行为控制

**建模示例：TCP连接状态**

```
状态: {CLOSED, SYN_SENT, SYN_RECEIVED, ESTABLISHED, FIN_WAIT_1,
       FIN_WAIT_2, CLOSE_WAIT, CLOSING, LAST_ACK, TIME_WAIT}

转移示例:
δ(CLOSED, active_open) = SYN_SENT
δ(SYN_SENT, syn_ack) = ESTABLISHED
δ(ESTABLISHED, close) = FIN_WAIT_1
```

#### 1.1.2 扩展状态机

**形式化定义**

扩展有限状态机（EFSM）引入变量和守卫条件：

$$EFSM = (S, I, O, V, T, s_0)$$

其中：

- $S$：状态集合
- $I$：输入集合
- $O$：输出集合
- $V$：变量集合
- $T \subseteq S \times G \times A \times S$：转移集合
  - $G$：守卫条件（布尔表达式）
  - $A$：动作（赋值/输出）
- $s_0$：初始状态

---

### 1.2 Petri网

#### 1.2.1 基本Petri网

**形式化定义**

Petri网是一个四元组 $PN = (P, T, F, M_0)$：

- $P = \{p_1, p_2, ..., p_m\}$：有限库所（place）集合
- $T = \{t_1, t_2, ..., t_n\}$：有限变迁（transition）集合，$P \cap T = \emptyset$
- $F \subseteq (P \times T) \cup (T \times P)$：流关系（弧集合）
- $M_0: P \rightarrow \mathbb{N}$：初始标识（marking）

**变迁使能规则**

变迁 $t \in T$ 在标识 $M$ 下使能（记为 $M[t\rangle$）当且仅当：

$$\forall p \in P: M(p) \geq W(p, t)$$

其中 $W(p, t)$ 为弧权重（缺省为1）。

**状态转移规则**

若 $M[t\rangle$，则 $M' = M - {}^\bullet t + t^\bullet$，即：

$$M'(p) = M(p) - W(p, t) + W(t, p), \quad \forall p \in P$$

**表达能力分析**

| 网类 | 表达能力 | 可判定性 |
|------|----------|----------|
| 状态机（State Machine） | 正则语言 | 可达性可判定 |
| 标识图（Marked Graph） | 并发系统 | 活性可判定 |
| 自由选择网（Free Choice） | 工作流 | 有界性可判定 |
| 普通Petri网 | 上下文相关 | 可达性可判定（复杂） |

**典型应用场景**

- 并发系统建模与分析
- 工作流验证
- 制造系统调度
- 通信协议验证

**建模示例：生产者-消费者问题**

```
库所: P={buffer_empty, buffer_full, producer_ready, consumer_ready}
变迁: T={produce, consume}

弧: F={(producer_ready, produce), (produce, buffer_full),
      (produce, producer_ready), (buffer_empty, produce),
      (buffer_full, consume), (consume, buffer_empty),
      (consumer_ready, consume), (consume, consumer_ready)}

初始标识: M0 = {buffer_empty:1, buffer_full:0,
                producer_ready:1, consumer_ready:1}
```

#### 1.2.2 有色Petri网（CPN）

**形式化定义**

有色Petri网是扩展的Petri网：

$$CPN = (\Sigma, P, T, A, N, C, G, E, I)$$

- $\Sigma$：颜色集合（数据类型）
- $P, T, A$：库所、变迁、弧
- $N: A \rightarrow (P \times T) \cup (T \times P)$：节点函数
- $C: P \rightarrow \Sigma$：颜色函数
- $G: T \rightarrow Expr$：守卫函数
- $E: A \rightarrow Expr$：弧表达式
- $I: P \rightarrow Expr$：初始化函数

**表达能力提升**

| 特性 | 基本Petri网 | 有色Petri网 |
|------|-------------|-------------|
| 令牌类型 | 无类型 | 可携带数据 |
| 模型大小 | 随实例数膨胀 | 参数化紧凑 |
| 表达能力 | 有限 | 图灵完备 |

#### 1.2.3 时序Petri网

**时间扩展**

- **Timed Petri网**：变迁有固定延迟
- **Time Petri网**：变迁有延迟区间 $[EFT, LFT]$
- **随机Petri网**：延迟服从概率分布

---

### 1.3 进程代数

#### 1.3.1 CSP（通信顺序进程）

**语法定义**

$$P ::= STOP \mid SKIP \mid a \rightarrow P \mid P \square Q \mid P \sqcap Q \mid P \parallel_A Q \mid P \setminus A \mid P[R] \mid \mu X \cdot F(X)$$

**语义**

1. **迹语义（Traces）**：$traces(P) \subseteq \Sigma^*$
2. **失败语义（Failures）**：$failures(P) \subseteq \Sigma^* \times \mathcal{P}(\Sigma)$
3. **发散语义（Divergences）**：处理非终止行为

**操作语义（SOS规则）**

$$
\frac{}{a \rightarrow P \xrightarrow{a} P} \quad \text{[Prefix]}
$$

$$
\frac{P \xrightarrow{a} P'}{P \square Q \xrightarrow{a} P'} \quad \text{[ExtChoice-L]}
$$

$$
\frac{P \xrightarrow{a} P', \quad a \notin A}{P \parallel_A Q \xrightarrow{a} P' \parallel_A Q} \quad \text{[Par-L]}
$$

$$
\frac{P \xrightarrow{a} P', \quad Q \xrightarrow{a} Q', \quad a \in A}{P \parallel_A Q \xrightarrow{a} P' \parallel_A Q'} \quad \text{[Par-Sync]}
$$

**典型应用场景**

- 并发程序验证
- 安全协议分析
- 操作系统设计
- FDR模型检验器

**建模示例：读者-写者问题**

```csp
READER = acquire_read -> read -> release_read -> READER
WRITER = acquire_write -> write -> release_write -> WRITER

RW_LOCK = (READER ||| WRITER)
          [|{|acquire_read, release_read,
              acquire_write, release_write|}|]
          LOCK_IMPL
```

#### 1.3.2 CCS（通信系统演算）

**语法定义**

$$P ::= 0 \mid \alpha.P \mid P + Q \mid P | Q \mid P \setminus L \mid P[f] \mid X \mid \text{rec } X.P$$

其中 $\alpha \in Act = \mathcal{N} \cup \overline{\mathcal{N}} \cup \{\tau\}$

**双模拟等价**

强双模拟：关系 $R$ 满足若 $(P, Q) \in R$ 且 $P \xrightarrow{\alpha} P'$，则存在 $Q \xrightarrow{\alpha} Q'$ 使得 $(P', Q') \in R$。

弱双模拟（观测等价）：忽略内部动作 $\tau$。

**表达能力对比**

| 特性 | CSP | CCS |
|------|-----|-----|
| 通信方式 | 基于事件 | 基于名称 |
| 选择算子 | 外部/内部选择 | 非确定性选择 |
| 隐藏操作 | 限制操作符 | 限制操作符 |
| 等价关系 | 失败/迹等价 | 双模拟等价 |

#### 1.3.3 π演算

**语法定义**

$$P ::= 0 \mid \pi.P \mid P + Q \mid P | Q \mid (\nu x)P \mid !P$$

其中 $\pi ::= x(y) \mid \overline{x}y \mid \tau$

**核心创新：移动性**

- 通道名可作为数据传递
- 支持动态重配置
- 表达能力：图灵完备

**形式化语义**

$$
\frac{}{x(y).P \xrightarrow{x(z)} P\{z/y\}} \quad \text{[Input]}
$$

$$
\frac{}{\overline{x}y.P \xrightarrow{\overline{x}y} P} \quad \text{[Output]}
$$

$$
\frac{P \xrightarrow{x(y)} P', \quad Q \xrightarrow{\overline{x}z} Q'}{P | Q \xrightarrow{\tau} P'\{z/y\} | Q'} \quad \text{[Comm]}
$$

**典型应用场景**

- 移动计算建模
- 动态网络协议
- 服务组合
- 生物系统建模

---

## 二、工作流模型

### 2.1 BPMN语义基础

#### 2.1.1 BPMN核心元素形式化

**形式化定义**

BPMN模型可形式化为：

$$BPMN = (N, E, T, G, D)$$

- $N = N_{activity} \cup N_{event} \cup N_{gateway}$：节点集合
- $E \subseteq N \times N$：顺序流
- $T: N_{activity} \rightarrow \{task, subprocess, call\}$：活动类型
- $G: N_{gateway} \rightarrow \{exclusive, parallel, inclusive, complex\}$：网关类型
- $D$：数据对象与关联

**网关语义**

**排他网关（XOR）**：
$$M_{out} = \{n_i \in N_{out} \mid guard_i(M) = true\}, \quad |M_{out}| = 1$$

**并行网关（AND）**：
$$M_{out} = N_{out}, \quad \text{要求所有输入令牌}
$$

**包容网关（OR）**：
$$M_{out} = \{n_i \in N_{out} \mid guard_i(M) = true\}, \quad |M_{out}| \geq 1$$

**表达能力分析**

| BPMN元素 | 表达能力 | 形式化映射 |
|----------|----------|------------|
| 顺序流 | 基本控制 | Petri网弧 |
| 排他网关 | 条件分支 | Petri网选择 |
| 并行网关 | 并发分叉/汇合 | Petri网AND-split/join |
| 事件 | 异步通信 | 有色Petri网 |
| 子流程 | 层次抽象 | 层次Petri网 |

**典型应用场景**

- 业务流程建模
- 工作流引擎实现
- 流程自动化
- 合规性验证

**建模示例：订单处理流程**

```bpmn
开始事件 -> 接收订单 -> 检查库存
  -> [库存充足] 并行网关 -> 打包 & 开发票 -> 并行汇合 -> 发货 -> 结束
  -> [库存不足] 采购 -> 检查库存
```

### 2.2 工作流网（WF-nets）

#### 2.2.1 形式化定义

工作流网是特殊Petri网：

$$WF = (P, T, F, i, o)$$

满足：

1. 存在唯一源库所 $i$，$\bullet i = \emptyset$
2. 存在唯一汇库所 $o$，$o^\bullet = \emptyset$
3. 每个节点在从 $i$ 到 $o$ 的路径上

**正确性标准**

**合理性（Soundness）**：

1. **可完成性**：从任何可达标识，总能到达 $[o]$
2. **正确完成**：当 $[o]$ 可达时，只有 $o$ 有令牌
3. **无死任务**：每个变迁都可在某个执行序列中触发

**形式化表述**：

$$\forall M \in R([i]): [o] \in R(M)$$

$$\forall M \in R([i]): M \geq [o] \Rightarrow M = [o]$$

$$
\forall t \in T: \exists M, M': M \xrightarrow{t} M'
$$

**扩展：带重置弧的WF-net**

引入重置弧 $R \subseteq T \times P$：

$$M' = (M - {}^\bullet t - R(t)) + t^\bullet$$

表达能力：可建模任意工作流模式

**典型应用场景**

- 工作流引擎核心模型
- 业务流程验证
- 流程挖掘
- 组织建模

### 2.3 YAWL（Yet Another Workflow Language）

#### 2.3.1 形式化定义

YAWL是扩展的工作流网：

$$YAWL = (N, C, E_{split}, E_{join}, A_{rem}, A_{cancel})$$

- $N$：基本WF-net
- $C$：条件集合
- $E_{split}, E_{join}$：分裂/汇合类型
  - AND, XOR, OR, Discriminator
- $A_{rem}$：移除域
- $A_{cancel}$：取消集

**高级模式支持**

| 模式 | YAWL支持 | 实现机制 |
|------|----------|----------|
| 多实例 | 是 | 动态实例创建 |
| 取消区域 | 是 | 取消集 |
| 同步合并 | 是 | Discriminator |
| 里程碑 | 是 | 状态检测 |
| 延迟选择 | 是 | OR-split |

**表达能力分析**

YAWL可表达全部20个基本工作流模式 + 23个高级模式。

**典型应用场景**

- 复杂业务流程建模
- 工作流模式研究
- 学术研究工具
- 流程设计验证

### 2.4 BPEL形式化

#### 2.4.1 BPEL核心结构形式化

**语法定义**

BPEL活动可递归定义：

$$
\begin{aligned}
A ::= & \text{invoke} \mid \text{receive} \mid \text{reply} \mid \text{assign} \mid \text{throw} \\
    & \mid \text{sequence}(A_1, ..., A_n) \mid \text{flow}(A_1, ..., A_n) \\
    & \mid \text{if}(cond, A_1, A_2) \mid \text{while}(cond, A) \\
    & \mid \text{pick}(onMessage_1 \rightarrow A_1, ..., onAlarm_n \rightarrow A_n) \\
    & \mid \text{scope}(A, handlers)
\end{aligned}
$$

**语义映射到Petri网**

| BPEL结构 | Petri网映射 |
|----------|-------------|
| sequence | 顺序连接 |
| flow | AND-split/join |
| if | XOR-split/join |
| while | 循环结构 |
| pick | 事件驱动选择 |
| scope | 层次化子网 |

**补偿处理形式化**

补偿处理器：
$$compensation(A) = A^{-1}$$

满足：
$$A ; A^{-1} \approx SKIP$$

**典型应用场景**

- Web服务编排
- 企业系统集成
- 长事务处理
- 业务流程执行

---

## 三、流计算模型

### 3.1 数据流模型

#### 3.1.1 Kahn进程网络（KPN）

**形式化定义**

Kahn进程网络是进程集合 $P = \{P_1, P_2, ..., P_n\}$，进程间通过无界FIFO通道通信。

**进程语义**

进程 $P_i$ 是函数：
$$P_i: S^{in}_i \rightarrow S^{out}_i$$

其中 $S$ 为无限流（序列）。

**确定性定理**

Kahn证明：KPN具有确定性的输入-输出行为，与执行顺序无关。

**形式化表述**：

$$\forall i, o: f_i(o) = f_i(\text{scheduling}(o))$$

**执行规则**

1. 读操作阻塞直到数据可用
2. 写操作非阻塞（假设无界通道）
3. 进程可任意交错执行

**表达能力分析**

| 特性 | KPN | 限制 |
|------|-----|------|
| 表达能力 | 图灵完备 | 无界内存 |
| 确定性 | 保证 | - |
| 调度 | 任意有效调度 | 死锁检测困难 |
| 实现 | 需要无界缓冲 | 实际系统截断 |

**典型应用场景**

- 信号处理系统
- 多媒体流处理
- 数据流语言（Lucid, Lustre）
- 图像处理管道

#### 3.1.2 同步数据流（SDF）

**形式化定义**

SDF是受限KPN，每个进程每次消费/生产固定数量的令牌。

SDF图：$G = (V, E, prod, cons)$

- $V$：进程（节点）集合
- $E \subseteq V \times V$：通道集合
- $prod: E \rightarrow \mathbb{N}^+$：生产速率
- $cons: E \rightarrow \mathbb{N}^+$：消费速率

**可调度性分析**

拓扑矩阵 $\Gamma$：行表示通道，列表示进程

$$
\Gamma_{e,v} = \begin{cases}
prod(e) & \text{if } v = src(e) \\
-cons(e) & \text{if } v = dst(e) \\
0 & \text{otherwise}
\end{cases}
$$

**可调度性条件**：

存在发射向量 $\vec{q} > 0$ 使得 $\Gamma \cdot \vec{q} = 0$

**缓冲区大小计算**

通过求解线性规划：

$$\min \sum_{e \in E} b_e$$

约束：$\Gamma \cdot \vec{q} = 0$，$b_e \geq \text{所需最小缓冲}$

**表达能力分析**

| 特性 | SDF | 扩展SDF |
|------|-----|---------|
| 调度 | 静态编译时确定 | 动态 |
| 缓冲区 | 静态计算 | 运行时分配 |
| 表达能力 | 有限（周期性） | 增强 |
| 复杂度 | 多项式时间 | NP-hard |

**典型应用场景**

- DSP编译器
- 实时信号处理
- 嵌入式系统
- 5G基带处理

**建模示例：FIR滤波器**

```
进程: Source -> [x1] -> Delay -> [x2] -> Delay -> [x3] -> Sum -> Sink
              |                          |
              +----> [c1] -> Mul <-------+
              |                          |
              +----> [c2] -> Mul <-------+
              |                          |
              +----> [c3] -> Mul <-------+

生产/消费速率: 每个节点每次消费/生产1个令牌
```

### 3.2 复杂事件处理（CEP）

#### 3.2.1 事件代数

**基本定义**

事件 $e = (id, type, ts, attrs)$

- $id$：唯一标识
- $type$：事件类型
- $ts$：时间戳
- $attrs$：属性集合

**事件流**

事件流 $S$ 是按时间排序的事件序列：

$$S = [e_1, e_2, ..., e_n], \quad ts(e_i) \leq ts(e_{i+1})$$

**操作符语义**

| 操作符 | 符号 | 语义 |
|--------|------|------|
| 过滤 | $\sigma_\phi(S)$ | 选择满足条件$\phi$的事件 |
| 映射 | $\mu_f(S)$ | 应用函数$f$到每个事件 |
| 窗口 | $\omega_{[t_1,t_2]}(S)$ | 选择时间范围内事件 |
| 连接 | $S_1 \bowtie_\theta S_2$ | 满足条件$\theta$的配对 |
| 序列 | $S_1 ; S_2$ | 模式匹配序列 |
| 选择 | $S_1 \mid S_2$ | 任一模式匹配 |

#### 3.2.2 事件模式形式化

**模式语法**

$$
\begin{aligned}
P ::= & E \mid P \cdot P \mid P \mid P \mid P^* \mid P^+ \\
    & \mid P \text{ WHERE } \phi \mid P \text{ WITHIN } t \\
    & \mid \neg P \mid P \text{ FOLLOWED BY } P
\end{aligned}
$$

**模式匹配语义**

模式 $P$ 在事件流 $S$ 上的匹配：

$$Match(P, S) = \{S' \subseteq S \mid S' \models P\}$$

**时间约束**

$$S' \models P \text{ WITHIN } t \iff S' \models P \land duration(S') \leq t$$

**典型应用场景**

- 金融欺诈检测
- 物联网监控
- 网络安全分析
- 业务流程监控

**建模示例：股票交易模式**

```
模式: 价格飙升后暴跌
      StockPrice(symbol=s, price>p1)
      FOLLOWED BY
      StockPrice(symbol=s, price>p1*1.05) WITHIN 5min
      FOLLOWED BY
      StockPrice(symbol=s, price<p1*0.95) WITHIN 10min
```

### 3.3 流处理系统形式化基础

#### 3.3.1 流处理算子代数

**基本算子**

| 算子 | 类型 | 语义 |
|------|------|------|
| map | $Stream\langle A \rangle \rightarrow Stream\langle B \rangle$ | $map(f)([a_1, a_2, ...]) = [f(a_1), f(a_2), ...]$ |
| filter | $Stream\langle A \rangle \rightarrow Stream\langle A \rangle$ | 选择满足谓词的元素 |
| flatMap | $Stream\langle A \rangle \rightarrow Stream\langle B \rangle$ | 一对多映射 |
| reduce | $Stream\langle A \rangle \rightarrow Stream\langle B \rangle$ | 聚合计算 |
| window | $Stream\langle A \rangle \rightarrow Stream\langle List\langle A \rangle \rangle$ | 分组为窗口 |
| join | $Stream\langle A \rangle \times Stream\langle B \rangle \rightarrow Stream\langle C \rangle$ | 流连接 |

**窗口类型形式化**

**滚动窗口（Tumbling）**：
$$W_{tumble}(S, size) = [S[0:size], S[size:2size], ...]$$

**滑动窗口（Sliding）**：
$$W_{slide}(S, size, step) = [S[0:size], S[step:size+step], ...]$$

**会话窗口（Session）**：
$$W_{session}(S, gap) = \text{按不活动间隙分割}$$

#### 3.3.2 一致性模型

**恰好一次语义**

$$\forall e \in Input: |\{e' \in Output \mid e' \text{ derived from } e\}| = 1$$

**实现机制**：

- 幂等性：$f(f(x)) = f(x)$
- 事务性提交
- 检查点与恢复

**时间语义**

| 时间类型 | 定义 | 用途 |
|----------|------|------|
| 事件时间 | 事件发生时间 | 业务逻辑 |
| 处理时间 | 处理到达时间 | 低延迟场景 |
| 摄入时间 | 进入系统时间 | 近似事件时间 |

**水位线（Watermark）**

$$WM(t) = \min_{e \in S}(ts(e)) - delay$$

保证时间戳小于 $WM(t)$ 的事件已到达。

**典型应用场景**

- 实时数据分析（Flink、Spark Streaming）
- 日志处理
- 推荐系统
- 实时监控告警

---

## 四、云原生模型

### 4.1 容器编排形式化

#### 4.1.1 Kubernetes调度理论

**形式化定义**

Kubernetes调度问题可建模为约束满足问题：

$$Schedule = (Pods, Nodes, Constraints, Objectives)$$

**约束类型**

| 约束 | 形式化 | 描述 |
|------|--------|------|
| 资源需求 | $\sum_{p \in node} res(p) \leq cap(node)$ | CPU/内存限制 |
| 节点选择器 | $node.labels \supseteq pod.nodeSelector$ | 标签匹配 |
| 亲和性 | $pod_A$ 与 $pod_B$ 同/反亲和 | 共置约束 |
| 污点容忍 | $pod.tolerations \cap node.taints \neq \emptyset$ | 特殊节点访问 |

**调度目标**

$$
\min \sum_{p \in Pods} cost(p, assigned\_node(p))
$$

**Pod生命周期状态机**

```
Pending -> [调度] -> ContainerCreating -> [镜像拉取] -> Running
                                              |
Running -> [终止] -> Terminating -> [清理] -> Succeeded/Failed
```

**形式化状态机**

$$M_{pod} = (\{Pending, Running, Succeeded, Failed, Unknown\}, \Sigma, \delta, Pending)$$

**典型应用场景**

- 容器编排系统
- 资源调度优化
- 自动扩缩容
- 高可用部署

#### 4.1.2 声明式配置语义

**期望状态与实际状态**

$$Spec: \text{期望状态} \quad Status: \text{实际状态}$$

**调和循环**

$$\text{Reconcile}(Spec, Status) = Actions$$

目标是使：

$$\lim_{t \rightarrow \infty} Status_t = Spec$$

**幂等性要求**

$$\text{Reconcile}(S, \text{Reconcile}(S, Status)) = \text{Reconcile}(S, Status)$$

### 4.2 微服务交互模型

#### 4.2.1 服务调用模式

**同步调用**

$$Client \xrightarrow{request} Server \xrightarrow{response} Client$$

形式化为请求-响应模式，超时处理：

$$timeout: \mathbb{T} \rightarrow \{success, failure\}$$

**异步调用**

$$Producer \xrightarrow{publish} MessageBus \xrightarrow{consume} Consumer$$

**调用链形式化**

分布式追踪：

$$Trace = (S, P, C)$$

- $S$：Span集合，每个Span = $(id, parent\_id, operation, timestamps)$
- $P$：进程/服务映射
- $C$：因果关系

**容错模式**

| 模式 | 形式化 | 语义 |
|------|--------|------|
| 超时 | $\Delta t > T_{max} \Rightarrow fail$ | 时间限制 |
| 重试 | $\sum_{i=1}^{n} attempt_i$ | 指数退避 |
| 熔断 | $failure\_rate > \theta \Rightarrow open$ | 故障隔离 |
| 限流 | $rate \leq R_{max}$ | 速率限制 |
| 降级 | $f_{fallback}(x)$ | 备用方案 |

**熔断器状态机**

$$M_{breaker} = (\{Closed, Open, HalfOpen\}, \{success, failure, timeout\}, \delta, Closed)$$

**典型应用场景**

- 微服务架构设计
- 服务网格实现
- 容错系统设计
- 性能优化

### 4.3 服务网格通信模型

#### 4.3.1 Sidecar代理模型

**架构形式化**

$$ServiceMesh = (Services, Proxies, ControlPlane)$$

通信路径：

$$Service_A \rightarrow Proxy_A \rightarrow Proxy_B \rightarrow Service_B$$

**流量管理**

| 功能 | 形式化 | 实现 |
|------|--------|------|
| 路由 | $route(request) \rightarrow destination$ | 权重/标签 |
| 负载均衡 | $select(endpoints, strategy)$ | 轮询/随机/最少连接 |
| 流量分割 | $\sum w_i = 1, \quad traffic_i = w_i \cdot total$ | A/B测试 |
| 故障注入 | $P(failure) = p$ | 混沌工程 |

**mTLS安全通道**

$$Channel = (Identity_A, Identity_B, Encrypted(SessionKey))$$

**典型应用场景**

- Istio/Linkerd实现
- 零信任网络
- 可观测性增强
- 多集群通信

### 4.4 无服务器计算模型

#### 4.4.1 函数即服务形式化

**函数生命周期**

$$Function = (Code, Runtime, Memory, Timeout, Environment)$$

**执行模型**

$$
Execution = \lambda(event). \begin{cases}
cold\_start & \text{if no warm instance} \\
warm\_invoke & \text{otherwise}
\end{cases}
$$

**冷启动延迟**

$$T_{cold} = T_{init} + T_{load} + T_{runtime}$$

**自动扩缩容**

$$Instances(t) = \lceil \frac{Concurrency(t)}{MaxConcurrencyPerInstance} \rceil$$

**计费模型**

$$Cost = N_{invocations} \cdot C_{invoke} + \sum_{i} T_{execution_i} \cdot Memory_i \cdot C_{memory}$$

**典型应用场景**

- 事件驱动处理
- API后端
- 数据处理管道
- 定时任务

---

## 五、新兴模型

### 5.1 Actor模型

#### 5.1.1 基本Actor模型

**形式化定义**

Actor系统：$AS = (A, M, B)$

- $A$：Actor集合，每个Actor有唯一地址
- $M$：消息集合
- $B$：行为函数

**Actor状态**

$$Actor = (Address, Behavior, Mailbox, State)$$

**操作原语**

1. **创建**：$create(B) \rightarrow Address$
2. **发送**：$send(Address, Message) \rightarrow \{\}$
3. **接收**：$receive(Mailbox) \rightarrow Message$

**语义规则**

$$
\frac{Actor_i \xrightarrow{send(j, m)} Actor_i'}{Mailbox_j' = Mailbox_j \cup \{m\}}
$$

$$
\frac{m \in Mailbox_i}{Actor_i \xrightarrow{process(m)} Actor_i'}
$$

**公平性**

$$\forall m \in Mailbox_i: \Diamond process(m)$$

**表达能力分析**

| 特性 | Actor模型 | 优势 |
|------|-----------|------|
| 并发 | 消息传递 | 无共享状态 |
| 容错 | 监督树 | 故障隔离 |
| 分布 | 位置透明 | 透明迁移 |
| 扩展 | 动态创建 | 弹性伸缩 |

**典型应用场景**

- 高并发系统（Akka、Erlang/OTP）
- 分布式计算
- 实时通信（WhatsApp）
- 游戏服务器

**建模示例：银行账户系统**

```erlang
actor Account(balance) {
  receive {
    Deposit(amount) ->
      become Account(balance + amount)
    Withdraw(amount) when balance >= amount ->
      become Account(balance - amount)
    GetBalance ->
      reply(balance)
      become Account(balance)
  }
}
```

#### 5.1.2 扩展Actor模型

**Akka Typed**

引入类型安全的消息协议：

$$Protocol = \{Message_1, Message_2, ..., Message_n\}$$

**Actor层次监督**

$$Supervisor = (Strategy, Children)$$

策略：$Strategy \in \{OneForOne, OneForAll, RestForOne\}$

### 5.2 CRDT理论

#### 5.2.1 形式化定义

**CRDT（Conflict-free Replicated Data Type）**

满足强最终一致性的数据类型：

$$CRDT = (S, \leq, \sqcup, s_0)$$

- $S$：状态集合
- $\leq$：偏序关系
- $\sqcup$：合并操作（least upper bound）
- $s_0$：初始状态

**CRDT性质**

1. **交换律**：$x \sqcup y = y \sqcup x$
2. **结合律**：$(x \sqcup y) \sqcup z = x \sqcup (y \sqcup z)$
3. **幂等律**：$x \sqcup x = x$

**收敛定理**

$$\forall replicas: \Diamond (state_i = state_j)$$

#### 5.2.2 CRDT类型

**基于状态的CRDT（CvRDT）**

$$merge(s_1, s_2) = s_1 \sqcup s_2$$

**基于操作的CRDT（CmRDT）**

$$prepare(op) \rightarrow effect(op, state)$$

要求操作满足：

- 交换律
- 因果传递

**常见CRDT实现**

| 数据类型 | 操作 | 合并策略 |
|----------|------|----------|
| G-Counter | increment | 取最大值 |
| PN-Counter | increment/decrement | 分解为两个G-Counter |
| G-Set | add | 并集 |
| OR-Set | add/remove | 唯一标签 |
| LWW-Register | write | 最后写入获胜 |
| MV-Register | write | 多版本 |

**典型应用场景**

- 协作编辑（Google Docs）
- 分布式数据库（Riak、Cassandra）
- 无冲突复制
- 离线优先应用

**建模示例：G-Counter**

```
状态: GCounter = Map<ReplicaId, Integer>

increment(r):
  GCounter[r]++

query():
  return sum(GCounter.values())

merge(GC1, GC2):
  return {r: max(GC1[r], GC2[r]) for r in keys}
```

### 5.3 共识算法形式化

#### 5.3.1 共识问题定义

**共识性质**

分布式系统中，$n$ 个进程对值 $v$ 达成共识：

1. **一致性（Agreement）**：
   $$\forall p_i, p_j: decided_i \land decided_j \Rightarrow v_i = v_j$$

2. **有效性（Validity）**：
   $$v \in \{proposed_1, ..., proposed_n\}$$

3. **终止性（Termination）**：
   $$\forall correct\ p_i: \Diamond decided_i$$

**FLP不可能结果**

在异步系统中，即使只有一个故障进程，也不存在确定性共识算法。

#### 5.3.2 Paxos形式化

**角色**

- Proposer：提出提案
- Acceptor：接受/拒绝提案
- Learner：学习已选值

**两阶段协议**

**Phase 1 (Prepare)**：

$$
\begin{aligned}
& Proposer \xrightarrow{Prepare(n)} Acceptors \\
& Acceptor_i \xrightarrow{Promise(n, (n', v'))} Proposer
\end{aligned}
$$

**Phase 2 (Accept)**：

$$
\begin{aligned}
& Proposer \xrightarrow{Accept(n, v)} Acceptors \\
& Acceptor_i \xrightarrow{Accepted(n, v)} Learners
\end{aligned}
$$

**安全条件**

$$\forall n_1 < n_2: chosen(n_1, v) \Rightarrow v_2 = v_1 \text{ or } v_2 \text{ undefined}$$

#### 5.3.3 Raft形式化

**状态机**

$$RaftNode = (State, CurrentTerm, VotedFor, Log[], CommitIndex)$$

$$State \in \{Follower, Candidate, Leader\}$$

**状态转换**

$$
\begin{aligned}
Follower & \xrightarrow{timeout} Candidate \\
Candidate & \xrightarrow{majority\ votes} Leader \\
Leader & \xrightarrow{higher\ term} Follower
\end{aligned}
$$

**日志复制**

$$
\frac{Entry_i.term = Entry_j.term \land Entry_i.index = Entry_j.index}{Entry_i.cmd = Entry_j.cmd}
$$

**安全性保证**

1. **选举安全**：最多一个Leader per term
2. **Leader完备性**：已提交日志在所有未来Leader中存在
3. **状态机安全**：相同索引的日志条目包含相同命令

**典型应用场景**

- 分布式数据库（etcd、Consul）
- 配置管理
- 分布式锁
- 复制状态机

### 5.4 区块链形式化模型

#### 5.4.1 区块链抽象模型

**形式化定义**

$$Blockchain = (Blocks, Txs, Consensus, Network)$$

**区块结构**

$$Block = (Header, Body)$$

$$Header = (PrevHash, MerkleRoot, Timestamp, Nonce, Difficulty)$$

$$Body = [Tx_1, Tx_2, ..., Tx_n]$$

**链式结构**

$$Chain = [Genesis, Block_1, Block_2, ..., Block_n]$$

$$\forall i > 0: Block_i.Header.PrevHash = Hash(Block_{i-1}.Header)$$

#### 5.4.2 共识机制形式化

**工作量证明（PoW）**

$$Find\ nonce: Hash(BlockHeader) < Target$$

$$Target = \frac{MaxTarget}{Difficulty}$$

**权益证明（PoS）**

$$P(validator_i) \propto Stake_i$$

**拜占庭容错（BFT）**

$$f < \frac{n}{3}$$

其中 $f$ 为拜占庭节点数，$n$ 为总节点数。

#### 5.4.3 智能合约形式化

**合约状态机**

$$Contract = (State, Methods, Invariants)$$

**执行语义**

$$\frac{State \vdash Method_i \Downarrow State'}{State \xrightarrow{Method_i} State'}$$

**安全性质**

| 性质 | 定义 | 攻击示例 |
|------|------|----------|
| 可重入安全 | 外部调用后状态一致 | DAO攻击 |
| 整数溢出安全 | 算术操作不溢出 | BEC代币 |
| 访问控制 | 权限检查完备 | Parity多签 |
| 原子性 | 操作全有或全无 | - |

**典型应用场景**

- 加密货币
- 去中心化金融（DeFi）
- 供应链管理
- 数字身份

---

## 六、模型对比与总结

### 6.1 表达能力层次

```
┌─────────────────────────────────────────────────────────────┐
│                    表达能力层次                              │
├─────────────────────────────────────────────────────────────┤
│  图灵完备层                                                 │
│  ├── Petri网（有色/时序）                                    │
│  ├── π演算                                                  │
│  ├── Actor模型                                              │
│  ├── 区块链智能合约                                          │
│  └── 数据流模型（KPN）                                       │
├─────────────────────────────────────────────────────────────┤
│  有限状态层                                                 │
│  ├── 有限状态机                                             │
│  ├── 基本Petri网                                            │
│  ├── SDF（同步数据流）                                       │
│  └── 工作流网                                               │
├─────────────────────────────────────────────────────────────┤
│  正则语言层                                                 │
│  └── 状态机（State Machine）Petri网                          │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 模型综合对比表

| 模型类别 | 代表模型 | 表达能力 | 可判定性 | 并发支持 | 分布式支持 | 典型工具 |
|----------|----------|----------|----------|----------|------------|----------|
| **经典模型** | | | | | | |
| 状态机 | FSM, Mealy, Moore | 正则语言 | 完全可判定 | 有限 | 无 | SPIN, UPPAAL |
| Petri网 | 基本/有色/时序 | 图灵完备 | 部分可判定 | 原生 | 扩展 | CPN Tools, Tina |
| 进程代数 | CSP, CCS, π | 图灵完备 | 双模拟可判定 | 原生 | π演算 | FDR, CADP |
| **工作流模型** | | | | | | |
| BPMN | BPMN 2.0 | 上下文相关 | 验证困难 | 原生 | 扩展 | Camunda, Activiti |
| WF-nets | 工作流网 | 上下文无关 | 合理性可判定 | 原生 | 无 | ProM, WoPeD |
| YAWL | YAWL | 图灵完备 | 部分可判定 | 原生 | 扩展 | YAWL Editor |
| BPEL | WS-BPEL | 上下文相关 | 验证困难 | 原生 | 原生 | Apache ODE |
| **流计算模型** | | | | | | |
| 数据流 | KPN, SDF | KPN图灵完备 | SDF可调度 | 原生 | 扩展 | Ptolemy, StreamIt |
| CEP | 事件代数 | 上下文相关 | 部分可判定 | 原生 | 扩展 | Esper, Flink CEP |
| 流处理 | 流算子代数 | 图灵完备 | 一致性可证 | 原生 | 原生 | Flink, Spark |
| **云原生模型** | | | | | | |
| 容器编排 | K8s调度理论 | NP-hard | 启发式 | 原生 | 原生 | Kubernetes |
| 微服务 | 交互模式 | 上下文相关 | 部分可判定 | 原生 | 原生 | Istio, Linkerd |
| Serverless | 函数模型 | 上下文相关 | 优化问题 | 原生 | 原生 | AWS Lambda |
| **新兴模型** | | | | | | |
| Actor | Actor模型 | 图灵完备 | 部分可判定 | 原生 | 原生 | Akka, Erlang |
| CRDT | 合并半格 | 收敛可证 | 一致性可证 | 原生 | 原生 | Riak, Redis |
| 共识 | Paxos/Raft | 安全性可证 | 活性可证 | 原生 | 原生 | etcd, ZooKeeper |
| 区块链 | 复制状态机 | 图灵完备 | 部分可判定 | 原生 | 原生 | Ethereum, Fabric |

### 6.3 模型选择决策树

```
需要形式化验证？
├── 是
│   ├── 状态空间有限？
│   │   ├── 是 → 状态机/模型检验
│   │   └── 否 → Petri网/进程代数
│   └── 需要并发分析？
│       ├── 是 → Petri网/CSP
│       └── 否 → 时序逻辑
└── 否
    ├── 工作流场景？
    │   ├── 标准流程 → BPMN
    │   ├── 需要验证 → WF-nets
    │   └── 复杂模式 → YAWL
    ├── 流处理场景？
    │   ├── 实时分析 → CEP
    │   ├── 大数据 → 流算子代数
    │   └── 嵌入式 → SDF
    ├── 云原生场景？
    │   ├── 容器编排 → K8s模型
    │   ├── 服务通信 → 微服务模型
    │   └── 事件驱动 → Serverless
    └── 分布式系统？
        ├── 高并发 → Actor模型
        ├── 最终一致 → CRDT
        ├── 共识需求 → Paxos/Raft
        └── 去信任 → 区块链
```

### 6.4 模型演进趋势

1. **从理论到实践**：形式化模型正在快速转化为工业级系统
2. **融合趋势**：不同模型的边界正在模糊（如Actor + CRDT）
3. **自动化验证**：模型检验与定理证明工具日益成熟
4. **云原生原生支持**：新模型设计考虑云环境特性
5. **形式化安全**：安全属性的形式化验证成为标准

---

## 附录：数学符号表

| 符号 | 含义 |
|------|------|
| $\rightarrow$ | 映射/函数 |
| $\Rightarrow$ | 蕴含 |
| $\Leftrightarrow$ | 等价 |
| $\forall$ | 全称量词 |
| $\exists$ | 存在量词 |
| $\Diamond$ | 最终（时序逻辑） |
| $\square$ | 总是（时序逻辑） |
| $\sqcup$ | 最小上界/合并 |
| $\vdash$ | 推导 |
| $\Downarrow$ | 求值 |
| $\bullet t$ | 变迁 $t$ 的前置集 |
| $t^\bullet$ | 变迁 $t$ 的后置集 |

---

*文档生成时间：2024年*
*作者：分布式计算模型专家*
