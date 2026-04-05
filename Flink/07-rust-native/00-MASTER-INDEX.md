# Flink + Rust + Assembly 生态系统 - 主索引

> **状态**: ✅ 全面更新完成 (2026-04-05) | **文档总数**: 45+ 篇 | **覆盖**: 9 大模块

---

## 📊 快速导航

### 🆕 新增核心文档（本次更新）

| 文档 | 路径 | 说明 | 大小 |
|------|------|------|------|
| **Iron Functions 完整指南** | [`iron-functions/01-iron-functions-complete-guide.md`](iron-functions/01-iron-functions-complete-guide.md) | 生产级 Rust UDF 方案 | 34KB |
| **Arroyo + Cloudflare 收购** | [`arroyo-update/01-arroyo-cloudflare-acquisition.md`](arroyo-update/01-arroyo-cloudflare-acquisition.md) | Rust 引擎重大事件 | 31KB |
| **Flash 生产验证 2025** | [`flash-engine/06-production-deployment-2025.md`](flash-engine/06-production-deployment-2025.md) | 阿里云 100K+ CUs 数据 | 22KB |
| **RisingWave Rust UDF** | [`risingwave-comparison/04-risingwave-rust-udf-guide.md`](risingwave-comparison/04-risingwave-rust-udf-guide.md) | 原生 `LANGUAGE rust` | 20KB |
| **Rust 引擎对比矩阵** | [`comparison/01-rust-streaming-engines-comparison.md`](comparison/01-rust-streaming-engines-comparison.md) | 7 大系统全面对比 | 20KB |
| **生态趋势 2026** | [`trends/01-flink-rust-ecosystem-trends-2026.md`](trends/01-flink-rust-ecosystem-trends-2026.md) | 五大趋势预测 | 34KB |

---

## 📁 模块完整目录

### 1. Iron Functions - 多语言 UDF

```
iron-functions/
└── 01-iron-functions-complete-guide.md  ⭐ 新增
```

**核心内容**: WASM UDF、Rust/Go/TypeScript、ironfun CLI、Ethereum 解码示例

### 2. Arroyo 更新 - Cloudflare 收购

```
arroyo-update/
├── 01-arroyo-cloudflare-acquisition.md  ⭐ 新增
├── PROGRESS-TRACKING.md                  📊 进展跟踪
├── IMPACT-ANALYSIS.md                    📊 影响分析
└── QUARTERLY-REVIEWS/
    └── 2026-Q2.md                        📊 季度回顾
```

**核心内容**: 2025年收购事件、Cloudflare Pipelines、10x 性能优势、持续进展跟踪

### 3. Flash 引擎 - 向量化执行

```
flash-engine/
├── 01-flash-architecture.md
├── 02-falcon-vector-layer.md
├── 03-forstdb-storage.md
├── 04-nexmark-benchmark-analysis.md
├── 05-flink-compatibility.md
└── 06-production-deployment-2025.md  ⭐ 新增
```

**核心内容**: C++ 向量化引擎、3-4x 性能、100% Flink 兼容、100K+ CUs 生产

### 4. RisingWave 对比

```
risingwave-comparison/
├── 01-risingwave-architecture.md
├── 02-nexmark-head-to-head.md
├── 03-migration-guide.md
├── 04-hybrid-deployment.md
└── 04-risingwave-rust-udf-guide.md  ⭐ 新增
```

**核心内容**: 流处理数据库、Rust 原生 UDF、PostgreSQL 协议

### 5. Rust 引擎对比

```
comparison/
└── 01-rust-streaming-engines-comparison.md  ⭐ 新增
```

**核心内容**: Flink vs Arroyo vs RisingWave vs Materialize vs ksqlDB

### 6. 趋势分析

```
trends/
└── 01-flink-rust-ecosystem-trends-2026.md  ⭐ 新增
```

**核心内容**: WASM UDF 标准化、向量化革命、Rust 引擎崛起、AI 原生流处理

### 7. SIMD 优化

```
simd-optimization/
├── 01-simd-fundamentals.md
├── 02-avx2-avx512-guide.md
├── 03-jni-assembly-bridge.md
├── 04-vectorized-udf-patterns.md
└── 05-arm-neon-sve-guide.md
```

**核心内容**: AVX2/AVX-512、ARM NEON/SVE、JNI 桥接、向量化模式

### 8. WASM 3.0

```
wasm-3.0/
├── 01-wasm-3.0-spec-guide.md
├── 02-memory64-deep-dive.md
├── 03-relaxed-simd-guide.md
└── 04-exception-handling-patterns.md
```

**核心内容**: Memory64、Relaxed SIMD、异常处理

### 9. WASI 0.3 异步

```
wasi-0.3-async/
├── 01-wasi-0.3-spec-guide.md
├── 02-async-streaming-patterns.md
├── 03-component-model-guide.md
└── 04-edge-compute-integration.md
```

**核心内容**: 异步流、组件模型、边缘计算

### 10. 其他模块

```
vectorized-udfs/          # 向量化 UDF (4篇)
heterogeneous-computing/  # 异构计算 (4篇)
edge-wasm-runtime/        # 边缘 Wasm (4篇)
ai-native-streaming/      # AI 原生流处理 (4篇)
```

---

## 🎯 学习路径推荐

### 路径 1: 快速上手 Rust UDF（1-2天）

1. [`iron-functions/01-iron-functions-complete-guide.md`](iron-functions/01-iron-functions-complete-guide.md) - Iron Functions 入门
2. [`risingwave-comparison/04-risingwave-rust-udf-guide.md`](risingwave-comparison/04-risingwave-rust-udf-guide.md) - 对比 RisingWave 原生方案
3. [`trends/01-flink-rust-ecosystem-trends-2026.md`](trends/01-flink-rust-ecosystem-trends-2026.md) - 了解趋势

### 路径 2: 引擎选型决策（2-3天）

1. [`comparison/01-rust-streaming-engines-comparison.md`](comparison/01-rust-streaming-engines-comparison.md) - 全面对比
2. [`flash-engine/06-production-deployment-2025.md`](flash-engine/06-production-deployment-2025.md) - Flash 引擎生产验证
3. [`arroyo-update/01-arroyo-cloudflare-acquisition.md`](arroyo-update/01-arroyo-cloudflare-acquisition.md) - Arroyo 最新动态

### 路径 3: 性能优化深度（3-5天）

1. [`simd-optimization/01-simd-fundamentals.md`](simd-optimization/01-simd-fundamentals.md) - SIMD 基础
2. [`flash-engine/01-flash-architecture.md`](flash-engine/01-flash-architecture.md) - 向量化架构
3. [`vectorized-udfs/01-vectorized-udf-intro.md`](vectorized-udfs/01-vectorized-udf-intro.md) - 向量化 UDF

---

## 📈 文档统计

| 指标 | 数值 |
|------|------|
| **总文档数** | 45+ 篇 |
| **新增文档** | 6 篇（本次更新） |
| **总大小** | ~600KB |
| **形式化定义** | 30+ 个 |
| **定理/命题** | 25+ 个 |
| **Mermaid 图表** | 50+ 个 |
| **代码示例** | 100+ 个 |

---

## 🔗 外部关键链接

- **Iron Functions**: <https://irontools.dev/>
- **Arroyo**: <https://www.arroyo.dev/>
- **RisingWave**: <https://www.risingwave.com/>
- **Apache Flink**: <https://flink.apache.org/>
- **Flash 引擎**: <https://www.alibabacloud.com/blog/flash>

---

*最后更新: 2026-04-05 | 更新者: Agent | 版本: v2.0*
