# TLA+ 形式化规约项目

> **所属阶段**: formal-methods/ Struct/ | 前置依赖: 分布式一致性理论基础 | 形式化等级: L5

本项目包含分布式系统中关键算法的 TLA+ 形式化规约，用于模型检测和性质验证。

---

## 📁 文件结构

```
formal-code/tla/
├── README.md                  # 本文件
├── TwoPhaseCommit.tla         # 两阶段提交协议完整规约
├── TwoPhaseCommit.cfg         # 两阶段提交 TLC 配置
├── Raft.tla                   # Raft 共识算法（基础框架）
├── Raft.cfg                   # Raft TLC 配置
├── Paxos.tla                  # Paxos 算法（基础框架）
├── Paxos.cfg                  # Paxos TLC 配置
└── common/
    └── Utilities.tla          # 通用工具模块
```

---

## 🛠️ 环境要求

### 安装 TLA+ Toolbox

1. **下载**: <https://lamport.azurewebsites.net/tla/toolbox.html>
2. **安装**: 根据操作系统选择对应版本
3. **验证**: 启动 TLA+ Toolbox

### 命令行工具（可选）

```bash
# macOS (使用 Homebrew)
brew install tlaplus

# 或下载社区版 TLC
# https://github.com/tlaplus/tlaplus/releases
```

---

## 🚀 如何运行 TLC 模型检测器

### 方法 1: 使用 TLA+ Toolbox（推荐）

1. **打开项目**
   - 启动 TLA+ Toolbox
   - File → Open Spec → 选择 `.tla` 文件

2. **创建模型**
   - TLC Model Checker → New Model
   - 指定模型名称

3. **配置常量**
   - 在 "Model Overview" 中设置常量值
   - 例如: `RM <- {r1, r2, r3}`

4. **配置检查项**
   - Invariants: 输入要检查的不变式（如 `TypeInvariant`）
   - Properties: 输入要验证的时序性质

5. **运行检测**
   - 点击 "Run TLC" 按钮
   - 查看结果和状态空间统计

### 方法 2: 命令行运行

```bash
# 进入项目目录
cd formal-methods/formal-code/tla

# 运行 TLC（需要 tla2tools.jar）
java -cp tla2tools.jar tlc2.TLC TwoPhaseCommit -config TwoPhaseCommit.cfg

# 或使用社区版命令
tlc TwoPhaseCommit.tla -config TwoPhaseCommit.cfg
```

---

## 📋 规约说明

### 1. TwoPhaseCommit (两阶段提交)

**文件**: `TwoPhaseCommit.tla`

**描述**: 经典的两阶段提交协议形式化规约，保证分布式事务的原子性。

**核心概念**:

- **RM (Resource Manager)**: 资源管理器，管理本地资源
- **TM (Transaction Manager)**: 事务管理器，协调全局事务

**状态定义**:

| 组件 | 状态 | 说明 |
|------|------|------|
| RM | "working" | 正常工作状态 |
| RM | "prepared" | 已准备提交 |
| RM | "committed" | 已提交 |
| RM | "aborted" | 已中止 |
| TM | "init" | 初始状态 |
| TM | "commit" | 决定提交 |
| TM | "abort" | 决定中止 |

**关键动作**:

- `RMAbort(r)`: RM 单方面中止事务
- `RMPrepare(r)`: RM 准备提交
- `TMCommit`: TM 决定提交所有 RM
- `TMAbort`: TM 决定中止事务

**验证性质**:

- `TypeInvariant`: 类型不变式
- `Consistency`: 一致性（所有 RM 不能同时处于 committed 和 aborted）
- `TMCommitImpliesAllPrepared`: TM 提交 implies 所有 RM 已准备

**运行建议**:

```
RM = {r1, r2, r3}  # 3个资源管理器
Ballot = {0, 1}    # 提案号范围
```

---

### 2. Raft (共识算法)

**文件**: `Raft.tla`

**描述**: Raft 共识算法的基础框架，基于 Diego Ongaro 的博士论文。

**核心概念**:

- **Server**: 服务器节点集合
- **Term**: 任期号，单调递增
- **Role**: 节点角色（Follower, Candidate, Leader）

**关键性质**:

- `ElectionSafety`: 每个任期最多一个 Leader
- `LeaderAppendOnly`: Leader 只追加日志，不修改/删除
- `LogMatching`: 如果两个日志条目有相同索引和任期，则内容相同
- `LeaderCompleteness`: 已提交的条目会被后续 Leader 保留
- `StateMachineSafety`: 状态机安全，已提交的命令按相同顺序执行

**状态空间**: 较大，建议使用较小的 Server 集合进行模型检测

---

### 3. Paxos (基础共识算法)

**文件**: `Paxos.tla`

**描述**: Leslie Lamport 的 Paxos 算法基础框架。

**核心概念**:

- **Acceptor**: 接受者集合
- **Proposer**: 提议者
- **Ballot**: 选票号，用于排序提议

**协议阶段**:

- **Phase 1a**: Proposer 发送 Prepare 请求
- **Phase 1b**: Acceptor 响应 Promise
- **Phase 2a**: Proposer 发送 Accept 请求
- **Phase 2b**: Acceptor 接受提议

**关键性质**:

- `Consistency`: 一致性，不同 Acceptor 不能接受不同值
- `Nontriviality`: 非平凡性，接受的值必须来自某个 Proposer

---

## 🧩 Utilities 模块

**文件**: `common/Utilities.tla`

提供通用工具和辅助函数：

- **集合操作**: 幂集、选择函数等
- **序列操作**: 序列操作符、前缀判断等
- **辅助函数**: 通用数学工具

使用方式：

```tla
EXTENDS common.Utilities
```

---

## 🔍 调试技巧

### 1. 状态空间爆炸

如果 TLC 运行时间过长：

- 减小常量集合的大小
- 使用对称性约简（Symmetry Set）
- 启用 "View" 优化

### 2. 错误追踪

当发现反例时：

- TLC 会生成错误轨迹
- 使用 "Error-Trace Exploration" 分析
- 检查每一步的状态变化

### 3. 性能优化

```tla
\* 在配置文件中启用 Workers
\* 使用多线程加速状态空间搜索
workers = 4
```

---

## 📚 参考资源

### 官方资源

- [TLA+ 主页](https://lamport.azurewebsites.net/tla/tla.html)
- [TLA+ 视频教程](https://lamport.azurewebsites.net/video/videos.html)
- [Learn TLA+](https://learntla.com/)

### 学术论文

1. Lamport, L. "Specifying Systems", 2002
2. Ongaro, D. "Consensus: Bridging Theory and Practice", 2014
3. Lamport, L. "The Part-Time Parliament", 1998

### 相关规约

- [TLA+ Examples](https://github.com/tlaplus/Examples)
- [Raft TLA+](https://github.com/ongardie/raft.tla)

---

## 📝 扩展计划

- [ ] 完善 Raft 完整规约（包含日志复制细节）
- [ ] 完善 Paxos 完整规约（包含 Multi-Paxos）
- [ ] 添加 Viewstamped Replication 规约
- [ ] 添加 Byzantine Fault Tolerance 规约
- [ ] 添加分布式事务 SAGA 模式规约

---

## 🏷️ 版本信息

- **版本**: 1.0.0
- **创建日期**: 2026-04-10
- **TLA+ 版本**: TLA+2
- **TLC 版本**: 2.18+
