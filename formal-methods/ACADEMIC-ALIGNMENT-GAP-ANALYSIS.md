# 国际顶尖大学课程对齐 - 差距分析报告

> **日期**: 2026-04-10 | **版本**: v1.0

---

## 📚 已调研的权威课程

### 美国顶尖大学

| 大学 | 课程代码 | 课程名称 | 核心内容 | 当前对齐状态 |
|------|---------|---------|---------|-------------|
| **MIT** | 6.826 | Principles of Computer Systems | Spec语言、并发/分布式系统、规范验证、同步机制、复制技术 | ⭐⭐⭐ 部分对齐 |
| **CMU** | 15-814 | Types and Programming Languages | PFPL教材、类型系统、λ演算、线性逻辑 | ⭐⭐⭐⭐ 较好对齐 |
| **Stanford** | CS 242 | Programming Languages | OCaml/Rust、类型系统、控制流、并发、元编程 | ⭐⭐⭐ 部分对齐 |
| **Berkeley** | CS 263 | Design of Programming Languages | 形式语义、类型系统、程序验证 | ⭐⭐ 待加强 |
| **UPenn** | CIS 500/670 | Software Foundations / Advanced PL | Coq基础、分离逻辑、高级类型系统 | ⭐⭐⭐ 部分对齐 |
| **Princeton** | COS 510 | Programming Languages | Coq、OCaml、形式化方法 | ⭐⭐⭐ 部分对齐 |

### 欧洲顶尖大学

| 大学 | 课程代码 | 课程名称 | 核心内容 | 当前对齐状态 |
|------|---------|---------|---------|-------------|
| **ETH Zurich** | - | Program Verification | Viper、Gobra、Prusti、分离逻辑 | ⭐⭐ 待加强 |
| **TU Munich** | IN2358 | Lambda Calculus | λ演算理论、归约、类型 | ⭐⭐⭐ 部分对齐 |
| **Cambridge** | - | Advanced PL | 范畴论、类型理论 | ⭐⭐ 待加强 |

---

## 🔍 详细差距分析

### 1. MIT 6.826 差距 ⭐⭐⭐

**已覆盖内容**:

- ✅ 并发系统基础
- ✅ 分布式系统概念
- ✅ 规范和验证基础
- ✅ 共识算法 (Paxos/Raft)

**缺失内容**:

- ❌ **Spec语言详解** - MIT 6.826使用Spec作为教学语言，我们缺少完整的Spec语言文档
- ❌ **实用并发** (Practical Concurrency) - 线程、锁、条件变量的形式化
- ❌ **命名系统形式化** (Naming) - 分布式命名系统的规范
- ❌ **网络对象** (Network Objects) - RPC的形式化语义
- ❌ **可用性与复制** - 更深入的分布式缓存管理
- ❌ **并发缓存一致性** - 缓存一致性协议的形式化

**建议新增文档**:

- `07-mit-spec-language.md` - Spec语言完整教程
- `08-practical-concurrency.md` - 实用并发形式化
- `09-distributed-naming.md` - 分布式命名系统

---

### 2. CMU 15-814 差距 ⭐⭐⭐⭐

**已覆盖内容**:

- ✅ 简单类型λ演算
- ✅ 多态 (System F)
- ✅ 类型安全性 (Preservation/Progress)
- ✅ Curry-Howard对应

**缺失内容**:

- ❌ **双向类型检查** (Bidirectional Type Checking) - 现代类型推断技术
- ❌ **递归类型** (Recursive Types) - μ类型、iso-recursive/equi-recursive
- ❌ **子类型** (Subtyping) - 记录子类型、函数子类型、有界量化
- ❌ **线性逻辑深入** - 资源敏感性、!A模态
- ❌ **高级类型系统** - 依赖类型入门、GADT

**建议新增文档**:

- `10-bidirectional-typechecking.md` - 双向类型检查
- `11-recursive-types.md` - 递归类型理论
- `12-subtyping.md` - 子类型系统

---

### 3. Stanford CS 242 差距 ⭐⭐⭐

**已覆盖内容**:

- ✅ λ演算基础
- ✅ 简单类型系统
- ✅ 多态

**缺失内容**:

- ❌ **JSON形式化** - 课程第一个作业是JSON形式化，我们缺少此类实用案例
- ❌ **WebAssembly形式化** - Wasm的类型系统和操作语义
- ❌ **Rust所有权系统** - 从类型理论角度深入分析
- ❌ **异步编程语义** - async/await的形式化
- ❌ **会话类型实现** - 用Rust类型系统实现会话类型
- ❌ **Lean定理证明** - 课程包含Lean实践，我们需要更多Lean内容

**建议新增文档**:

- `13-json-formalization.md` - JSON形式化案例
- `14-webassembly-semantics.md` - WebAssembly语义
- `15-rust-ownership-types.md` - Rust所有权类型理论
- `16-async-semantics.md` - 异步编程语义

---

### 4. ETH Zurich Program Verification 差距 ⭐⭐

**已覆盖内容**:

- ✅ 分离逻辑基础
- ✅ Hoare逻辑

**缺失内容**:

- ❌ **Viper验证基础设施** - 工业级验证工具，极其重要！
- ❌ **权限推理** (Permission-based Reasoning) - 访问权限的形式化
- ❌ **Gobra** - Go语言验证器
- ❌ **Prusti深入** - 我们提到Prusti但缺少详细教程
- ❌ **Nagini** - Python验证器
- ❌ **weakest precondition计算** - 验证条件生成
- ❌ **循环不变式推断** - 自动化技术
- ❌ **Ghost状态** - 辅助验证的幽灵状态

**建议新增文档**:

- `17-viper-tutorial.md` - Viper完整教程
- `18-permission-based-reasoning.md` - 权限推理
- `19-weakest-precondition.md` - 最弱前置条件
- `20-loop-invariants.md` - 循环不变式

---

### 5. Iris 高阶并发分离逻辑 差距 ⭐⭐

**已覆盖内容**:

- ✅ 分离逻辑基础
- ✅ 并发程序验证概念

**缺失内容**:

- ❌ **Iris框架完整教程** - 当前最重要的分离逻辑框架！
- ❌ **高阶逻辑** - 命题作为资源
- ❌ **Later Modality** (▷) - 步进索引
- ❌ **Persistently Modality** (□) - 持久性模态
- ❌ **Invariants** - 并发不变式
- ❌ **Ghost State** - 幽灵状态和资源代数
- ❌ **Atomic Specifications** - 原子性规范
- ❌ **Logical Relations** - 在Iris中定义逻辑关系

**建议新增文档**:

- `21-iris-tutorial.md` - Iris完整教程（必读！）
- `22-higher-order-separation-logic.md` - 高阶分离逻辑
- `23-ghost-state.md` - 幽灵状态
- `24-logical-relations-iris.md` - Iris逻辑关系

---

### 6. Rust验证生态 差距 ⭐⭐⭐

**已覆盖内容**:

- ✅ RustBelt提及
- ✅ Prusti提及

**缺失内容**:

- ❌ **Creusot详细教程** - 基于Why3的Rust验证器
- ❌ **Kani** - Amazon的Rust模型检查器
- ❌ **Verus** - 微软的Rust验证器
- ❌ **Flux** - 精化类型检查器
- ❌ **Aeneas** - 基于λ演算的Rust验证
- ❌ **Gillian-Rust** - 混合验证方法
- ❌ **RefinedRust** - 基础验证
- ❌ **Rust标准库验证项目** - Amazon领导的大型项目

**建议新增文档**:

- `25-rust-verification-landscape.md` - Rust验证全景
- `26-creusot-tutorial.md` - Creusot教程
- `27-kani-verifier.md` - Kani模型检查器
- `28-verus-tutorial.md` - Verus教程

---

## 📊 优先级矩阵

| 内容 | 学术价值 | 工业价值 | 教学价值 | 综合优先级 |
|------|---------|---------|---------|-----------|
| Iris分离逻辑 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **P0** |
| Viper基础设施 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **P0** |
| Rust验证生态 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **P0** |
| Spec语言 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | **P1** |
| 双向类型检查 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | **P1** |
| WebAssembly语义 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | **P1** |
| 递归类型 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | **P2** |
| 子类型 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **P2** |
| 异步语义 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **P2** |
| 权限推理 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | **P2** |

---

## 🎯 后续任务计划

### Phase E: 前沿验证技术对齐 (建议下一优先)

#### P0 任务 (最高优先级)

1. **Iris高阶并发分离逻辑完整文档**
   - 预计工作量: 10-12天
   - 内容: 完整的Iris教程，包含所有模态、幽灵状态、案例研究
   - 对齐课程: UPenn CIS 670, MIT 6.826

2. **Viper验证基础设施文档**
   - 预计工作量: 8-10天
   - 内容: Viper语言教程、权限推理、Gobra/Prusti/Nagini介绍
   - 对齐课程: ETH Zurich Program Verification

3. **Rust验证生态全景**
   - 预计工作量: 8-10天
   - 内容: Creusot、Kani、Verus、Flux等工具的详细教程
   - 对齐课程: Rust Formal Methods Interest Group

#### P1 任务 (高优先级)

1. **MIT Spec语言教程**
   - 预计工作量: 6-8天
   - 内容: Spec语言语法、规范编写、案例研究
   - 对齐课程: MIT 6.826

2. **双向类型检查与推断**
   - 预计工作量: 5-7天
   - 内容: 双向类型检查算法、Hindley-Milner推断
   - 对齐课程: CMU 15-814, Stanford CS 242

3. **WebAssembly形式化语义**
   - 预计工作量: 5-7天
   - 内容: Wasm类型系统、操作语义、验证案例
   - 对齐课程: Stanford CS 242

#### P2 任务 (中优先级)

1. **递归类型理论**
   - 预计工作量: 4-6天
   - 对齐课程: CMU 15-814

2. **子类型系统**
   - 预计工作量: 4-6天
   - 对齐课程: CMU 15-814, Stanford CS 242

3. **异步编程语义**
   - 预计工作量: 4-6天
   - 对齐课程: Stanford CS 242

4. **实用并发形式化**
    - 预计工作量: 5-7天
    - 对齐课程: MIT 6.826

---

## 📈 预期成果

完成Phase E后，项目将：

1. **完整对齐ETH Zurich** - Viper生态是ETH的招牌
2. **领先覆盖Iris** - 目前网络上最完整的Iris中文资源
3. **最全面的Rust验证资源** - 覆盖所有主流Rust验证工具
4. **补充MIT 6.826** - Spec语言和实用并发
5. **加强CMU/Stanford** - 现代类型系统特性

---

## ✅ 请确认

请审阅以上差距分析和任务计划，确认：

1. **优先级是否正确？** P0/P1/P2分级是否合理？
2. **任务范围是否合适？** 每个任务的预计工作量是否合理？
3. **是否有遗漏的重要课程？** 是否还有其他顶尖大学的课程需要补充？
4. **开始执行哪些任务？** 建议从P0开始全面并行推进

---

*报告生成时间: 2026-04-10*
*调研大学: MIT, CMU, Stanford, Berkeley, UPenn, Princeton, ETH Zurich, TU Munich, Cambridge*
