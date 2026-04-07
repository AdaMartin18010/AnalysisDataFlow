# 交叉引用索引 (Cross-Reference Index)

> **所属阶段**: Knowledge/Flink-Scala-Rust-Comprehensive/99-appendix | 版本: v1.0 | 覆盖文档: 28+

---

## 目录

- [交叉引用索引 (Cross-Reference Index)](#交叉引用索引-cross-reference-index)
  - [目录](#目录)
  - [1. 文档导航](#1-文档导航)
    - [1.1 按章节组织](#11-按章节组织)
      - [01 - Scala 流编程生态](#01---scala-流编程生态)
      - [02 - Flink 技术体系](#02---flink-技术体系)
      - [03 - Scala ↔ Rust 互操作](#03---scala--rust-互操作)
      - [04 - Rust 流处理引擎](#04---rust-流处理引擎)
      - [05 - 架构模式](#05---架构模式)
      - [06 - 2026 趋势](#06---2026-趋势)
      - [99 - 附录](#99---附录)
    - [1.2 按角色导航](#12-按角色导航)
    - [1.3 按技术栈导航](#13-按技术栈导航)
  - [2. 形式化定义索引](#2-形式化定义索引)
    - [2.1 定义类型统计](#21-定义类型统计)
    - [2.2 按类别索引](#22-按类别索引)
      - [Scala 类型系统 (Def-K-01-*, Def-K-SC-*)](#scala-类型系统-def-k-01--def-k-sc-)
      - [Flink 架构 (Def-K-02-\*)](#flink-架构-def-k-02-)
      - [WASM/WASI (Def-K-WSI-\*)](#wasmwasi-def-k-wsi-)
      - [Rust 引擎 (Def-RUST-*, Def-RW-*, Def-MZ-\*)](#rust-引擎-def-rust--def-rw--def-mz-)
    - [2.3 定理与证明索引](#23-定理与证明索引)
    - [2.4 引理索引](#24-引理索引)
  - [3. 代码示例索引](#3-代码示例索引)
    - [3.1 按语言分类](#31-按语言分类)
      - [Scala 代码示例](#scala-代码示例)
      - [Rust 代码示例](#rust-代码示例)
      - [Java 代码示例](#java-代码示例)
      - [SQL 代码示例](#sql-代码示例)
      - [配置示例](#配置示例)
    - [3.2 按主题分类](#32-按主题分类)
  - [4. 图表索引](#4-图表索引)
    - [4.1 Mermaid 图表统计](#41-mermaid-图表统计)
    - [4.2 关键架构图索引](#42-关键架构图索引)
    - [4.3 流程图索引](#43-流程图索引)
    - [4.4 时序图索引](#44-时序图索引)
  - [5. 主题快速查找](#5-主题快速查找)
    - [5.1 核心概念查找表](#51-核心概念查找表)
    - [5.2 常见问题解答索引](#52-常见问题解答索引)
    - [5.3 性能优化指南索引](#53-性能优化指南索引)
  - [6. 依赖关系图](#6-依赖关系图)
    - [6.1 文档依赖关系](#61-文档依赖关系)
    - [6.2 前置依赖矩阵](#62-前置依赖矩阵)
  - [附录：索引使用指南](#附录索引使用指南)
    - [快速查找技巧](#快速查找技巧)
    - [交叉引用格式](#交叉引用格式)

---

## 1. 文档导航

### 1.1 按章节组织

#### 01 - Scala 流编程生态

| 文档编号 | 文档名称 | 关键主题 | 形式化等级 |
|----------|----------|----------|------------|
| 01.01 | [scala-streaming-landscape](../01-scala-ecosystem/01.01-scala-streaming-landscape.md) | Scala 流生态、fs2、Pekko Streams、ZIO | L4 |
| 01.02 | [flink-scala-api-analysis](../01-scala-ecosystem/01.02-flink-scala-api-analysis.md) | Flink Scala API、类型安全、互操作 | L4 |
| 01.03 | [scala-java-api-interop](../01-scala-ecosystem/01.03-scala-java-api-interop.md) | Scala/Java 互操作、API 兼容 | L3 |
| 01.04 | [fs2-pekko-streams](../01-scala-ecosystem/01.04-fs2-pekko-streams.md) | fs2、Pekko Streams 对比、集成 | L4 |
| 01.05 | [scala-type-system-streaming](../01-scala-ecosystem/01.05-scala-type-system-streaming.md) | HKT、Type Class、宏编程 | L5 |

#### 02 - Flink 技术体系

| 文档编号 | 文档名称 | 关键主题 | 形式化等级 |
|----------|----------|----------|------------|
| 02.01 | [flink-2x-architecture](../02-flink-system/02.01-flink-2x-architecture.md) | Flink 2.x、存算分离、Adaptive Scheduler | L5 |
| 02.02 | [flink-runtime-deep-dive](../02-flink-system/02.02-flink-runtime-deep-dive.md) | 运行时、Checkpoint、网络栈 | L4 |
| 02.03 | [flink-state-backends](../02-flink-system/02.03-flink-state-backends.md) | State Backend、ForSt、RocksDB | L4 |
| 02.04 | [flink-sql-table-api](../02-flink-system/02.04-flink-sql-table-api.md) | SQL、Table API、Streaming SQL | L4 |
| 02.05 | [flink-cloud-native](../02-flink-system/02.05-flink-cloud-native.md) | K8s、Operator、云原生部署 | L3 |

#### 03 - Scala ↔ Rust 互操作

| 文档编号 | 文档名称 | 关键主题 | 形式化等级 |
|----------|----------|----------|------------|
| 03.01 | [wasm-interop](../03-scala-rust-interop/03.01-wasm-interop.md) | WASM、WASI 0.3、组件模型 | L4 |
| 03.02 | [jni-bridge](../03-scala-rust-interop/03.02-jni-bridge.md) | JNI、unsafe、FFI 性能 | L4 |
| 03.03 | [grpc-service](../03-scala-rust-interop/03.03-grpc-service.md) | gRPC、服务网格、分布式 | L3 |
| 03.04 | [iron-functions-guide](../03-scala-rust-interop/03.04-iron-functions-guide.md) | Iron Functions、WASM UDF | L3 |
| 03.05 | [interop-comparison](../03-scala-rust-interop/03.05-interop-comparison.md) | 互操作方案对比、选型决策 | L3 |

#### 04 - Rust 流处理引擎

| 文档编号 | 文档名称 | 关键主题 | 形式化等级 |
|----------|----------|----------|------------|
| 04.01 | [rust-engines-comparison](../04-rust-engines/04.01-rust-engines-comparison.md) | 引擎对比、选型决策 | L4 |
| 04.02 | [risingwave-deep-dive](../04-rust-engines/04.02-risingwave-deep-dive.md) | RisingWave、Hummock、物化视图 | L4 |
| 04.03 | [materialize-analysis](../04-rust-engines/04.03-materialize-analysis.md) | Materialize、Differential Dataflow | L4 |
| 04.04 | [arroyo-cloudflare](../04-rust-engines/04.04-arroyo-cloudflare.md) | Arroyo、Cloudflare、边缘计算 | L3 |
| 04.05 | [vectorization-simd](../04-rust-engines/04.05-vectorization-simd.md) | SIMD、向量化、性能优化 | L4 |

#### 05 - 架构模式

| 文档编号 | 文档名称 | 关键主题 | 形式化等级 |
|----------|----------|----------|------------|
| 05.01 | [hybrid-architecture-patterns](../05-architecture-patterns/05.01-hybrid-architecture-patterns.md) | 混合架构、分层设计 | L3 |
| 05.02 | [migration-strategies](../05-architecture-patterns/05.02-migration-strategies.md) | 迁移策略、渐进式改造 | L3 |
| 05.03 | [cloud-deployment](../05-architecture-patterns/05.03-cloud-deployment.md) | 多云部署、K8s 最佳实践 | L3 |
| 05.04 | [edge-computing](../05-architecture-patterns/05.04-edge-computing.md) | 边缘计算、低延迟架构 | L3 |

#### 06 - 2026 趋势

| 文档编号 | 文档名称 | 关键主题 | 形式化等级 |
|----------|----------|----------|------------|
| 06.01 | [2026-trends](../06-trends-2026/06.01-2026-trends.md) | 技术趋势、演进预测 | L2 |
| 06.02 | [adoption-roadmap](../06-trends-2026/06.02-adoption-roadmap.md) | 采纳路线图、决策框架 | L2 |

#### 99 - 附录

| 文档编号 | 文档名称 | 关键主题 | 形式化等级 |
|----------|----------|----------|------------|
| 99.01 | [glossary](99.01-glossary.md) | 术语表、定义索引 | L1 |
| 99.02 | [references](99.02-references.md) | 参考文献、资源索引 | L1 |
| 99.03 | [cross-reference-index](cross-reference-index.md) | 交叉引用、快速查找 | L1 |

---

### 1.2 按角色导航

| 角色 | 推荐文档路径 |
|------|-------------|
| **架构师** | 05.01 → 05.03 → 05.04 → 06.01 → 06.02 |
| **Scala 开发者** | 01.01 → 01.02 → 01.04 → 01.05 → 03.02 |
| **Rust 开发者** | 04.01 → 04.02 → 03.01 → 04.05 |
| **Flink 用户** | 02.01 → 02.02 → 02.03 → 01.02 → 02.04 |
| **运维工程师** | 02.05 → 05.03 → 05.04 → 02.01 |
| **性能工程师** | 04.05 → 02.03 → 04.02 → 02.02 |
| **技术决策者** | 04.01 → 06.01 → 06.02 → 05.01 |

---

### 1.3 按技术栈导航

| 技术领域 | 核心文档 | 扩展阅读 |
|----------|----------|----------|
| **Scala 流编程** | 01.01, 01.04, 01.05 | 01.02, 01.03 |
| **Flink 核心** | 02.01, 02.02, 02.03 | 02.04, 02.05 |
| **Rust 流引擎** | 04.01, 04.02, 04.03 | 04.04, 04.05 |
| **WASM 互操作** | 03.01, 03.04 | 03.05 |
| **云原生部署** | 02.05, 05.03 | 05.01, 05.04 |
| **架构设计** | 05.01, 05.02, 06.01 | 06.02 |

---

## 2. 形式化定义索引

### 2.1 定义类型统计

| 类型 | 前缀 | 数量 | 说明 |
|------|------|------|------|
| 定义 | Def-K-* | 45+ | Knowledge 层形式化定义 |
| 引理 | Lemma-K-* | 25+ | 从定义推导的性质 |
| 命题 | Prop-K-* | 20+ | 需要证明的声明 |
| 定理 | Thm-K-* | 15+ | 主要形式化结果 |
| 推论 | Cor-K-* | 5+ | 从定理直接推导 |

### 2.2 按类别索引

#### Scala 类型系统 (Def-K-01-*, Def-K-SC-*)

| 编号 | 名称 | 位置 | 描述 |
|------|------|------|------|
| Def-K-01-01 | Scala 流编程生态系统 | 01.01 | 五元组形式化定义 |
| Def-K-01-02 | 函数式流处理 | 01.01 | 引用透明与惰性求值 |
| Def-K-01-03 | 流类型构造子 | 01.01 | HKT 形式化 |
| Def-K-SC-01 | Type Class 模型 | 01.05 | 类型类形式化 |
| Def-K-SC-02 | Higher-Kinded Types | 01.05 | 高阶类型构造子 |

#### Flink 架构 (Def-K-02-*)

| 编号 | 名称 | 位置 | 描述 |
|------|------|------|------|
| Def-K-02-01 | 存算分离架构 | 02.01 | DisaggregatedArch 五元组 |
| Def-K-02-02 | 统一调度器 | 02.01 | Adaptive Scheduler 定义 |
| Def-K-02-03 | 异步检查点增强 | 02.01 | Checkpoint O(1) 复杂度 |
| Def-K-02-04 | 异步执行模型 | 02.01 | 非阻塞状态访问 |
| Def-K-02-05 | ForSt State Backend | 02.03 | 云原生状态后端 |

#### WASM/WASI (Def-K-WSI-*)

| 编号 | 名称 | 位置 | 描述 |
|------|------|------|------|
| Def-K-WSI-01 | WASI 系统接口 | 03.01 | 四元组形式化 |
| Def-K-WSI-02 | WASI 0.3 异步 I/O 模型 | 03.01 | AsyncWASI 定义 |
| Def-K-WSI-03 | WASM 组件模型 | 03.01 | Component 定义 |

#### Rust 引擎 (Def-RUST-*, Def-RW-*, Def-MZ-*)

| 编号 | 名称 | 位置 | 描述 |
|------|------|------|------|
| Def-RUST-01 | Rust 原生流处理引擎 | 04.01 | 四元组定义 |
| Def-RUST-02 | 一致性模型层次 | 04.01 | 一致性偏序关系 |
| Def-RUST-03 | 流处理引擎分类学 | 04.01 | Taxonomy 定义 |
| Def-RW-01 | 流处理数据库 | 04.02 | StreamingDB 定义 |
| Def-RW-02 | 计算存储分离架构 | 04.02 | SepArch 定义 |
| Def-RW-03 | Hummock 分层存储引擎 | 04.02 | 三层存储定义 |

### 2.3 定理与证明索引

| 编号 | 名称 | 位置 | 类型 | 描述 |
|------|------|------|------|------|
| Thm-K-01-01 | Scala 流库的范畴论统一 | 01.01 | 定理 | Monad 统一抽象 |
| Thm-K-02-01 | 分离存储下的 Exactly-Once | 02.01 | 定理 | 存算分离语义保持 |
| Thm-K-02-02 | Adaptive Scheduler 收敛性 | 02.01 | 定理 | 调度器收敛证明 |
| Thm-K-WSI-01 | 异步 UDF 吞吐量定理 | 03.01 | 定理 | WASI 性能优势 |
| Thm-K-WSI-02 | 类型安全形式化论证 | 03.01 | 证明 | WIT 类型一致性 |
| Thm-RUST-01 | 选型决策定理 | 04.01 | 定理 | 最优选择公式 |
| Thm-RW-01 | RisingWave Exactly-Once | 04.02 | 证明 | Epoch-based 保证 |
| Thm-RW-02 | Rust UDF 执行性能定理 | 04.02 | 定理 | 原生 UDF 优势 |

### 2.4 引理索引

| 编号 | 名称 | 位置 | 描述 |
|------|------|------|------|
| Lemma-K-01-01 | Scala 流库的组合性 | 01.01 | 适配器模式组合 |
| Lemma-K-01-02 | 纯函数流变换的确定性 | 01.01 | 输出确定性保证 |
| Lemma-K-02-01 | 存算分离扩缩容灵活性 | 02.01 | O(1) 扩缩容复杂度 |
| Lemma-K-02-02 | 异步模型资源利用率 | 02.01 | CPU 利用率提升 |
| Lemma-RW-01 | 计算节点无状态性 | 04.02 | 无状态证明 |
| Lemma-RW-02 | 水平扩展线性加速 | 04.02 | 扩展效率公式 |

---

## 3. 代码示例索引

### 3.1 按语言分类

#### Scala 代码示例

| 文档 | 示例名称 | 描述 |
|------|----------|------|
| 01.01 | fs2 基础流操作 | Stream、map、filter、fold |
| 01.01 | Pekko Streams 图构建 | Source、Flow、Sink、GraphDSL |
| 01.01 | ZIO Streams 效应集成 | ZStream、资源安全、背压 |
| 01.02 | Flink Scala API | DataStream、类型安全 |
| 01.04 | 跨库互操作 | fs2↔Pekko↔ZIO 转换 |
| 03.01 | Scala WASM 宿主封装 | WasiProcessor 实现 |
| 03.02 | JNI 绑定代码 | Scala↔Rust JNI 调用 |

#### Rust 代码示例

| 文档 | 示例名称 | 描述 |
|------|----------|------|
| 03.01 | Rust WASM 模块开发 | WIT、async、WASI 0.3 |
| 03.02 | JNI 原生方法实现 | unsafe、FFI、JNI 导出 |
| 04.02 | Rust UDF 开发 | #[udf] 宏、SIMD 优化 |
| 04.05 | SIMD 向量化 | AVX2、auto-vectorization |

#### Java 代码示例

| 文档 | 示例名称 | 描述 |
|------|----------|------|
| 02.01 | Async State API | 异步状态访问 Java API |
| 02.02 | ProcessFunction | 低级别流处理 |
| 03.01 | Flink WASM UDF 集成 | FlinkWasiUdfJob |

#### SQL 代码示例

| 文档 | 示例名称 | 描述 |
|------|----------|------|
| 02.04 | Flink SQL 窗口查询 | TUMBLE、HOP、SESSION |
| 04.01 | 引擎 SQL 对比 | RisingWave/Materialize/Arroyo |
| 04.02 | RisingWave 物化视图 | CREATE MATERIALIZED VIEW |

#### 配置示例

| 文档 | 示例名称 | 描述 |
|------|----------|------|
| 02.01 | Flink 2.x YAML 配置 | 存算分离、Adaptive Scheduler |
| 02.05 | K8s Deployment | FlinkDeployment CRD |
| 04.02 | RisingWave K8s 部署 | Compute/Meta/Compactor |
| 05.03 | 多云部署配置 | AWS/Azure/GCP |

### 3.2 按主题分类

| 主题 | 相关代码示例 | 主要文档 |
|------|-------------|----------|
| **流基础操作** | map/filter/fold/window | 01.01, 01.04 |
| **类型安全** | Type Class、HKT | 01.05 |
| **状态管理** | State Backend、Checkpoint | 02.03 |
| **异步编程** | async/await、Future | 03.01 |
| **互操作** | WASM、JNI、gRPC | 03.01-03.05 |
| **性能优化** | SIMD、向量化 | 04.05 |
| **部署配置** | YAML、K8s、Helm | 02.05, 05.03 |

---

## 4. 图表索引

### 4.1 Mermaid 图表统计

| 类型 | 数量 | 主要用途 |
|------|------|----------|
| graph TB/TD | 25+ | 架构图、层次结构 |
| flowchart | 15+ | 决策树、流程图 |
| sequenceDiagram | 8+ | 时序图、调用链 |
| classDiagram | 3+ | 类型结构 |
| stateDiagram | 2+ | 状态机 |
| quadrantChart | 2+ | 对比矩阵 |
| radar | 1+ | 能力雷达图 |

### 4.2 关键架构图索引

| 图名称 | 位置 | 描述 |
|--------|------|------|
| Scala 流生态系统全景图 | 01.01 | fs2/Pekko/ZIO/Flink 关系 |
| Flink 1.x vs 2.x 架构对比 | 02.01 | 存算分离演进 |
| Adaptive Scheduler 决策流程 | 02.01 | 自动扩缩容决策 |
| WASI 0.3 异步执行模型 | 03.01 | Scala↔Rust 异步调用 |
| RisingWave 整体架构 | 04.02 | 分层存储架构 |
| Flink vs RisingWave 架构对比 | 04.02 | 架构差异对比 |
| Rust 引擎能力雷达图 | 04.01 | RisingWave/Materialize/Arroyo |
| 技术选型决策树 | 04.01 | 引擎选型指南 |

### 4.3 流程图索引

| 图名称 | 位置 | 描述 |
|--------|------|------|
| WASI 0.2 vs 0.3 选型决策 | 03.01 | 异步 I/O 选型 |
| 流库选型决策矩阵 | 01.01 | fs2/Pekko/ZIO 选择 |
| 互操作方案对比矩阵 | 03.05 | WASM/JNI/gRPC 选择 |
| 引擎选型决策树 | 04.01 | 引擎选择流程 |
| 迁移策略流程 | 05.02 | 渐进式迁移 |

### 4.4 时序图索引

| 图名称 | 位置 | 描述 |
|--------|------|------|
| WASI 0.3 异步执行模型 | 03.01 | Scala→WASM→I/O 调用链 |
| Rust UDF 执行流程 | 04.02 | 注册→编译→执行流程 |
| Flink Checkpoint 协调 | 02.02 | JM→TM 协调流程 |
| gRPC 服务调用链 | 03.03 | Scala↔Rust gRPC 调用 |

---

## 5. 主题快速查找

### 5.1 核心概念查找表

| 概念 | 定义位置 | 实现示例 | 相关定理 |
|------|----------|----------|----------|
| **存算分离** | 02.01 (Def-K-02-01) | ForSt 配置 | Thm-K-02-01 |
| **异步状态访问** | 02.01 (Def-K-02-04) | AsyncValueState | Lemma-K-02-02 |
| **WASI 0.3** | 03.01 (Def-K-WSI-02) | Rust WASM 模块 | Thm-K-WSI-01 |
| **物化视图** | 04.02 (Def-RW-01) | CREATE MATERIALIZED VIEW | Thm-RW-01 |
| **Hummock** | 04.02 (Def-RW-03) | 三层存储配置 | Lemma-RW-03 |
| **Type Class** | 01.05 | Functor/Monad 实现 | Thm-K-01-01 |

### 5.2 常见问题解答索引

| 问题 | 答案位置 |
|------|----------|
| Flink 2.x 有哪些新特性？ | 02.01 第 1-2 节 |
| 如何选择 Scala 流库？ | 01.01 第 5 节，01.04 第 6 节 |
| WASI 0.3 vs 0.2 怎么选？ | 03.01 第 4.2 节 |
| RisingWave 和 Flink 区别？ | 04.02 第 3 节 |
| SIMD 在流处理中如何应用？ | 04.05 第 5 节 |
| K8s 上如何部署 Flink 2.x？ | 02.05 第 6 节 |
| 如何实现 Scala↔Rust 互操作？ | 03.01-03.05 |
| 流处理引擎如何选型？ | 04.01 第 5 节，06.02 |

### 5.3 性能优化指南索引

| 优化方向 | 相关文档 | 关键技术 |
|----------|----------|----------|
| **状态访问** | 02.03, 04.02 | ForSt, Hummock 缓存 |
| **向量化** | 04.05 | SIMD, AVX2 |
| **异步 I/O** | 02.01, 03.01 | async/await, WASI 0.3 |
| **并行度调优** | 02.01, 02.02 | Adaptive Scheduler |
| **内存管理** | 04.01, 04.05 | Rust 所有权, Arrow |

---

## 6. 依赖关系图

### 6.1 文档依赖关系

```
00-MASTER-INDEX
    │
    ├── 01-scala-ecosystem/
    │       ├── 01.01 (基础) ──┬──► 01.02 ──┬──► 01.04
    │       │                  │            │
    │       └── 01.05 (类型) ◄─┘            └──► 01.03
    │
    ├── 02-flink-system/
    │       ├── 02.01 (架构) ──┬──► 02.02 ──┬──► 02.03
    │       │                  │            │
    │       └── 02.05 ◄────────┴──► 02.04 ◄─┘
    │
    ├── 03-scala-rust-interop/
    │       ├── 03.01 (WASM) ──┬──► 03.04
    │       ├── 03.02 (JNI) ◄──┤
    │       ├── 03.03 (gRPC) ◄─┤
    │       └── 03.05 (对比) ◄─┘
    │
    ├── 04-rust-engines/
    │       ├── 04.01 (对比) ──┬──► 04.02
    │       │                  ├──► 04.03
    │       │                  ├──► 04.04
    │       │                  └──► 04.05
    │
    ├── 05-architecture-patterns/
    │       └── 05.01 → 05.02 → 05.03 → 05.04
    │
    ├── 06-trends-2026/
    │       └── 06.01 → 06.02
    │
    └── 99-appendix/
            └── 99.01, 99.02, cross-reference-index
```

### 6.2 前置依赖矩阵

| 文档 | 强依赖 | 弱依赖 |
|------|--------|--------|
| 01.02 | 01.01 | Flink 基础 |
| 01.03 | 01.02 | JVM 基础 |
| 01.04 | 01.01 | Reactive Streams |
| 01.05 | 01.01 | 范畴论基础 |
| 02.02 | 02.01 | 网络基础 |
| 02.03 | 02.01, 02.02 | 存储基础 |
| 02.04 | 02.01 | SQL 基础 |
| 02.05 | 02.01 | K8s 基础 |
| 03.01 | - | WASM/WASI 基础 |
| 03.02 | 03.01 | JNI 基础 |
| 03.03 | - | gRPC 基础 |
| 03.04 | 03.01 | Serverless 基础 |
| 03.05 | 03.01-03.04 | - |
| 04.01 | - | 流处理基础 |
| 04.02 | 04.01 | 数据库基础 |
| 04.03 | 04.01 | 一致性模型基础 |
| 04.04 | 04.01 | 边缘计算基础 |
| 04.05 | 04.01 | SIMD 基础 |
| 05.01 | 02.01, 04.01 | 架构设计基础 |
| 05.02 | 05.01 | 迁移经验 |
| 05.03 | 02.05, 05.01 | 云平台经验 |
| 05.04 | 05.03 | 边缘部署经验 |
| 06.01 | 全部 | 行业洞察 |
| 06.02 | 06.01, 全部 | 决策框架 |

---

## 附录：索引使用指南

### 快速查找技巧

1. **查找术语定义**：使用 [99.01-glossary.md](99.01-glossary.md) 按类别浏览
2. **查找参考文献**：使用 [99.02-references.md](99.02-references.md) 的类别索引
3. **查找形式化定义**：使用本文第 2 节的定义索引表
4. **查找代码示例**：使用本文第 3 节的分类索引
5. **查找图表**：使用本文第 4 节的图表索引

### 交叉引用格式

- 文档引用：`[章节.文档号-名称](../路径/文件.md)`
- 定义引用：`Def-K-{文档号}-{序号}`
- 定理引用：`Thm-K-{文档号}-{序号}`
- 引理引用：`Lemma-K-{文档号}-{序号}`
- 文献引用：`[^{n}]`

---

*文档版本: v1.0 | 创建日期: 2026-04-07 | 覆盖文档: 28篇 | 总索引项: 300+*
