# 流计算性能测试套件

本目录包含完整的流计算性能测试框架，用于评估 Flink、RisingWave、Materialize 等流处理引擎的性能。

## 目录结构

```
performance-tests/
├── nexmark-benchmark-suite.md      # Nexmark 基准测试文档
├── simd-vectorization-benchmark.md # SIMD 向量化性能测试
├── wasm-udf-overhead-analysis.md   # WASM UDF 开销测试
├── performance-test-framework.md   # 性能测试框架文档
├── README.md                       # 本文件
│
├── nexmark/                        # Nexmark 测试实现
│   ├── flink/                      # Flink Scala 实现
│   │   ├── pom.xml
│   │   └── src/main/scala/nexmark/
│   ├── risingwave/                 # RisingWave SQL
│   └── materialize/                # Materialize SQL
│
├── simd/                           # SIMD 向量化测试
│   ├── rust/                       # Rust SIMD 实现
│   │   ├── Cargo.toml
│   │   ├── src/
│   │   └── benches/
│   └── java/                       # Java Vector API
│       └── VectorizedOperations.java
│
└── wasm/                           # WASM UDF 测试
    ├── rust/                       # Rust WASM 实现
    ├── java/                       # JNI 对比
    └── scala/                      # Flink WASM 集成
```

## 快速开始

### 1. 环境要求

- JDK 11+
- Scala 2.12
- Rust 1.75+
- Apache Flink 1.18+
- Python 3.9+ (用于报告生成)

### 2. 运行 Nexmark 测试

```bash
cd nexmark/flink
mvn clean package

# 运行 Q5 测试
flink run -p 4 target/nexmark-flink-1.0-SNAPSHOT.jar \
  --query Q5 \
  --parallelism 4 \
  --max-events 10000000 \
  --events-per-second 100000
```

### 3. 运行 SIMD 测试

```bash
cd simd/rust
cargo bench

# 查看报告
target/criterion/report/index.html
```

### 4. 运行 WASM 测试

```bash
cd wasm/rust
# 编译 WASM
cargo build --target wasm32-unknown-unknown --release

# 运行基准测试
cargo bench
```

## 主要发现

| 测试类型 | 关键发现 |
|---------|---------|
| Nexmark | RisingWave 在复杂 Join 上比 Flink 快 1.5-2x |
| SIMD | AVX-512 可达 6-7x 加速比，选择率影响较小 |
| WASM | 调用开销 10-50x，适合复杂业务逻辑而非简单计算 |

## 文档清单

1. **nexmark-benchmark-suite.md** (40002 字节)
   - Nexmark 查询集完整定义 (Q0-Q12)
   - Flink/RisingWave/Materialize 实现
   - 性能对比结果与图表

2. **simd-vectorization-benchmark.md** (15162 字节)
   - SIMD 测试设计方法论
   - Rust AVX2/AVX-512/NEON 实现
   - Java Vector API 实现

3. **wasm-udf-overhead-analysis.md** (17554 字节)
   - WASM vs JNI vs Native 对比
   - 函数调用/数据传输开销测试
   - 选型决策树

4. **performance-test-framework.md** (21144 字节)
   - 测试框架架构设计
   - JMH + Criterion 集成
   - 统计分析与可视化

**总文档大小**: ~94KB
**总代码行数**: 2000+ 行
