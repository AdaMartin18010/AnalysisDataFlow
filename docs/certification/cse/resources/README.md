# CSE 学习资源

> **高级认证学习资料汇总** | 形式化理论与架构设计

## 形式化理论基础

### 进程演算

| 文档 | 难度 | 预计时间 | 重点 |
|------|------|----------|------|
| [进程演算入门](../../../../Struct/01-foundations/01.01-process-calculus-intro.md) | ★★★★☆ | 4h | CCS/CSP/π-calculus |
| [Actor vs 进程演算](../../../../Struct/01-foundations/01.02-actor-vs-process-calculus.md) | ★★★★☆ | 3h | 模型对比 |

### 类型理论

| 文档 | 难度 | 预计时间 | 重点 |
|------|------|----------|------|
| [流计算的会话类型](../../../../Struct/01-foundations/01.03-session-types-for-streaming.md) | ★★★★★ | 5h | Session Types |
| [状态管理的线性类型](../../../../Struct/01-foundations/01.04-linear-types-state-management.md) | ★★★★★ | 4h | Linear Types |

### 一致性理论

| 文档 | 难度 | 预计时间 | 重点 |
|------|------|----------|------|
| [Exactly-Once 形式化语义](../../../../Struct/02-properties/02.01-exactly-once-semantics.md) | ★★★★★ | 4h | 语义定义 |
| [一致性层次](../../../../Struct/02-properties/02.02-consistency-hierarchy.md) | ★★★★☆ | 3h | 层次模型 |
| [Watermark 单调性](../../../../Struct/02-properties/02.03-watermark-monotonicity.md) | ★★★★★ | 3h | 定理证明 |

### 形式化验证

| 文档 | 难度 | 预计时间 | 重点 |
|------|------|----------|------|
| [TLA+ for Flink](../../../../Struct/06-verification/06.01-tla-plus-for-flink.md) | ★★★★☆ | 4h | TLA+ 应用 |
| [Checkpoint 模型检测](../../../../Struct/06-verification/06.02-model-checking-checkpoint.md) | ★★★★★ | 4h | 模型检测 |

## 经典文献

### 进程演算奠基论文

1. **R. Milner** - "A Calculus of Communicating Systems" (1980)
   - CCS 原始论文
   - 奠定了进程代数基础

2. **C.A.R. Hoare** - "Communicating Sequential Processes" (1978, 1985)
   - CSP 经典著作
   - 迹语义与失败语义

3. **R. Milner** - "The Polyadic π-calculus: A Tutorial" (1993)
   - π-calculus 移动性理论

### 流计算理论

1. **T. Akidau et al.** - "The Dataflow Model" (VLDB 2015)
   - 现代流计算理论奠基
   - 核心概念：Watermark、窗口、触发器

2. **T. Akidau et al.** - "Streaming Systems" (Book, 2018)
   - 流计算系统理论与实践

### 一致性理论

1. **M. Herlihy & J. Wing** - "Linearizability: A Correctness Condition for Concurrent Objects" (TOPLAS 1990)
   - 线性一致性经典定义

2. **S. Burckhardt** - "Principles of Eventual Consistency" (FnT 2014)
   - 最终一致性系统综述

### 形式化验证

1. **L. Lamport** - "The Temporal Logic of Actions" (TOPLAS 1994)
   - TLA 时序逻辑

2. **R. Jung et al.** - "Iris from the Ground Up" (2018)
   - Iris 高阶并发分离逻辑

## 工具与软件

### TLA+ 工具链

```bash
# TLA+ Toolbox
wget https://github.com/tlaplus/tlaplus/releases/download/v1.7.1/TLAToolbox-1.7.1-linux.gtk.x86_64.zip

# Community Modules
git clone https://github.com/tlaplus/CommunityModules.git
```

### 定理证明器

- **Coq**: <https://coq.inria.fr/>
- **Isabelle/HOL**: <https://isabelle.in.tum.de/>
- **Lean**: <https://leanprover.github.io/>

### 模型检测器

- **FDR4** (CSP): <https://www.cs.ox.ac.uk/projects/fdr/>
- **SPIN** (Promela): <http://spinroot.com/>
- **NuSMV**: <http://nusmv.fbk.eu/>

## 在线课程

### 形式化方法

| 课程 | 机构 | 链接 |
|------|------|------|
| Formal Methods | CMU 15-814 | [课程页面](https://www.cs.cmu.edu) |
| Logic and Proof | Stanford CS151 | [课程页面](https://stanford.edu) |
| Interactive Computer Theorem Proving | MIT 6.887 | [课程页面](https://mit.edu) |

### 分布式系统理论

| 课程 | 机构 | 链接 |
|------|------|------|
| Distributed Systems | MIT 6.824 | [课程页面](https://pdos.csail.mit.edu/6.824/) |
| Advanced Operating Systems | CMU 15-712 | [课程页面](https://www.cs.cmu.edu) |

## 研究工具

### 文献管理

- **Zotero**: <https://www.zotero.org/>
- **Mendeley**: <https://www.mendeley.com/>
- **JabRef**: <https://www.jabref.org/>

### 论文写作

- **Overleaf**: <https://www.overleaf.com/> (LaTeX 在线协作)
- **Authorea**: <https://www.authorea.com/>
- **TeXstudio**: <https://www.texstudio.org/>

### 图表绘制

- **Draw.io**: <https://app.diagrams.net/>
- **TikZ**: LaTeX 绘图宏包
- **Graphviz**: 自动图布局

## 学术会议与期刊

### 形式化方法

- **CAV**: Computer Aided Verification
- **TACAS**: Tools and Algorithms for Construction and Analysis of Systems
- **FMCAD**: Formal Methods in Computer-Aided Design
- **POPL**: Principles of Programming Languages

### 分布式系统

- **PODC**: Principles of Distributed Computing
- **DISC**: International Symposium on Distributed Computing
- **OSDI**: Operating Systems Design and Implementation
- **SOSP**: Symposium on Operating Systems Principles

### 数据库与流计算

- **VLDB**: Very Large Data Bases
- **SIGMOD**: ACM Conference on Management of Data
- **ICDE**: International Conference on Data Engineering
- **CIDR**: Conference on Innovative Data Systems Research

## 架构设计资源

### 案例研究

- [LinkedIn Brooklin](https://github.com/linkedin/brooklin)
- [Uber AthenaX](https://github.com/uber/AthenaX)
- [Netflix Keystone](https://netflixtechblog.com/)
- [Apache Kafka](https://kafka.apache.org/documentation/)

### 设计模式

- [Knowledge/05-architecture-patterns/](../../../../Knowledge/05-architecture-patterns/)
- [DEPLOYMENT-ARCHITECTURES.md](../../../../DEPLOYMENT-ARCHITECTURES.md)

## 论文选题建议

### 形式化验证方向

1. **流计算算子的形式化语义**
   - 目标: 为 Flink DataStream API 建立形式化语义
   - 工具: TLA+, Coq

2. **Watermark 算法的正确性证明**
   - 目标: 证明 Watermark 算法保证窗口完整性
   - 工具: Isabelle/HOL

3. **一致性协议的验证**
   - 目标: 验证自定义一致性协议的正确性
   - 工具: TLA+, TLC

### 架构设计方向

1. **大规模流平台架构**
   - 目标: 设计支持每秒亿级事件的流平台
   - 产出: 架构文档 + POC

2. **边缘-云协同计算架构**
   - 目标: 设计边云协同的流处理框架
   - 产出: 架构文档 + 原型

## 导师匹配

根据研究方向，系统会为您匹配相应领域的导师：

| 研究方向 | 导师类型 | 代表机构 |
|----------|----------|----------|
| 形式化验证 | 高校教授/研究员 | 清华、北大、中科院 |
| 分布式系统 | 企业研究员 | 阿里巴巴、微软亚研 |
| 流计算架构 | 资深架构师 | 字节跳动、美团 |
| 数据库系统 | 开源 Committer | Apache 项目 PMC |

---

[返回课程大纲 →](../syllabus-cse.md)
