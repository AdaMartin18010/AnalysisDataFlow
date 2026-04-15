# RisingWave Rust UDF 原生语法完整指南

> **所属阶段**: Flink/ | **前置依赖**: [01-risingwave-architecture.md, risingwave-comparison/03-migration-guide.md] | **形式化等级**: L4 (工程实践)
>
> **文档编号**: RW-UDF-01 | **版本**: v1.0 | **日期**: 2026-04-05

---

## 1. 概念定义 (Definitions)

### Def-RW-17: RisingWave Rust UDF 双模式架构

**定义**: RisingWave Rust UDF 支持两种执行模式，形成互补的 UDF 能力矩阵 $\mathcal{U}_{RW}$:

$$
\mathcal{U}_{RW} = \langle \mathcal{U}_{embedded}, \mathcal{U}_{wasm}, \mathcal{M}_{select} \rangle
$$

其中：

- $\mathcal{U}_{embedded}$: 嵌入式 Rust UDF（`LANGUAGE rust`），直接在数据库进程内执行
- $\mathcal{U}_{wasm}$: WebAssembly UDF（`LANGUAGE wasm`），在沙箱化 WASM 运行时中执行
- $\mathcal{M}_{select}: \mathcal{Q} \to \{\mathcal{U}_{embedded}, \mathcal{U}_{wasm}\}$: 基于查询特征的自动/手动选择函数

**模式选择决策函数**:

$$
\mathcal{M}_{select}(q) = \begin{cases}
\mathcal{U}_{embedded} & \text{if } \text{latency}(q) < 100\mu s \land \text{complexity}(q) = \text{simple} \\
\mathcal{U}_{wasm} & \text{if } \text{isolation}(q) = \text{required} \lor \text{portability}(q) = \text{cross-platform}
\end{cases}
$$

---

### Def-RW-18: 嵌入式 Rust UDF 语义模型

**定义**: 嵌入式 Rust UDF 是一种在 RisingWave 计算节点进程内直接执行的函数，其形式化语义为：

$$
\mathcal{U}_{embedded} = \langle \Sigma, \Gamma, \mathcal{F}, \mathcal{T} \rangle
$$

其中：

- $\Sigma$: Rust 类型系统，包含 SQL-Rust 类型映射 $\sigma: \text{SQLType} \to \text{RustType}$
- $\Gamma$: 函数签名上下文，$\Gamma \vdash f: \tau_1 \times \tau_2 \times ... \times \tau_n \to \tau_{out}$
- $\mathcal{F}$: 函数体实现，符合 Rust 语法和所有权规则
- $\mathcal{T}$: 执行语义，零开销抽象，直接内存访问

**语法形式**:

```sql
CREATE FUNCTION function_name(arg_type, ...)
RETURNS return_type
LANGUAGE rust
AS $$
    // Rust 函数体
$$;
```

---

### Def-RW-19: WASM UDF 沙箱执行模型

**定义**: WASM UDF 在 RisingWave 内置的 WebAssembly 运行时中执行，提供语言无关的隔离执行环境：

$$
\mathcal{U}_{wasm} = \langle \mathcal{M}_{wasm32}, \mathcal{I}_{arrow}, \mathcal{S}_{sandbox}, \mathcal{L}_{link} \rangle
$$

其中：

- $\mathcal{M}_{wasm32}$: wasm32-wasip1 目标模块，遵循 WASI 预览1 规范
- $\mathcal{I}_{arrow}$: Arrow 格式数据接口，零拷贝列式数据传输
- $\mathcal{S}_{sandbox}$: 能力导向安全模型，细粒度权限控制
- $\mathcal{L}_{link}$: 模块链接策略（BASE64 内嵌或文件系统链接）

**编译目标链**:

```
Rust 源码 → LLVM IR → WASM 字节码 → WASI 运行时 → RisingWave UDF 注册
```

---

### Def-RW-20: SQL-Rust 类型同构映射

**定义**: 类型映射函数 $\sigma$ 定义 SQL 类型与 Rust 类型之间的双向同构关系：

$$
\sigma: \mathcal{T}_{SQL} \xrightarrow{\cong} \mathcal{T}_{Rust}
$$

满足：

$$
\forall t \in \mathcal{T}_{SQL}: \sigma^{-1}(\sigma(t)) = t
$$

**核心类型映射表**:

| SQL 类型 | Rust 类型 | 备注 |
|---------|-----------|------|
| `BOOLEAN` | `bool` | 直接映射 |
| `SMALLINT` | `i16` | 有符号 16 位 |
| `INTEGER` | `i32` | 有符号 32 位 |
| `BIGINT` | `i64` | 有符号 64 位 |
| `REAL` | `f32` | IEEE 754 单精度 |
| `DOUBLE` | `f64` | IEEE 754 双精度 |
| `VARCHAR` | `String` / `&str` | UTF-8 编码 |
| `BYTEA` | `Vec<u8>` / `&[u8]` | 二进制数据 |
| `DATE` | `chrono::NaiveDate` | 日期类型 |
| `TIME` | `chrono::NaiveTime` | 时间类型 |
| `TIMESTAMP` | `chrono::NaiveDateTime` | 无时区时间戳 |
| `TIMESTAMPTZ` | `chrono::DateTime<UTC>` | UTC 时间戳 |
| `DECIMAL` | `rust_decimal::Decimal` | 精确小数 |
| `INTERVAL` | `chrono::Duration` | 时间间隔 |
| `JSONB` | `serde_json::Value` | JSON 数据 |
| `ARRAY<T>` | `Vec<T>` | 动态数组 |
| `STRUCT<...>` | `#[derive(StructType)]` | 自定义结构体 |

---

## 2. 属性推导 (Properties)

### Prop-RW-14: 嵌入式 Rust UDF 零开销特性

**命题**: 嵌入式 Rust UDF 满足零开销抽象原则，即对于简单标量函数 $f_{scalar}$，执行开销满足：

$$
T_{exec}(f_{scalar}) \approx T_{native}(f_{scalar}) + \epsilon_{call}
$$

其中 $\epsilon_{call} < 50ns$ 为函数调用开销。

**证明概要**:

1. 嵌入式 UDF 在计算节点进程内执行，无 IPC 开销
2. 数据通过内存指针直接传递，无序列化/反序列化
3. Rust 编译器内联优化消除函数调用边界
4. 因此 $\epsilon_{call}$ 仅为边界检查和安全包装的开销 $\square$

---

### Prop-RW-15: WASM UDF 隔离完备性

**命题**: WASM UDF 提供进程级隔离安全性，恶意或错误的 UDF 代码无法：

1. 访问 RisingWave 进程内存空间 $M_{RW}$
2. 执行系统调用（除显式声明的 WASI 能力外）
3. 造成内存泄漏影响数据库稳定性

**形式化**: 设 WASM 模块内存空间为 $M_{wasm}$，则：

$$
M_{wasm} \cap M_{RW} = \emptyset \land \forall op \in \text{SystemCall}: \text{capability}(op) \subseteq \text{declared}
$$

---

### Prop-RW-16: 表函数迭代器惰性求值

**命题**: RisingWave 表函数（Table Function）采用惰性迭代器语义，输出批次大小 $B$ 满足：

$$
B = \min(B_{requested}, B_{available})
$$

即每次迭代按需生成结果，避免物化整个结果集。

**优势**:

- 内存使用 $O(1)$ 相对于输出大小
- 支持无限流生成（如 `series()` 生成无限整数序列）
- 提前终止优化（LIMIT 下推）

---

## 3. 关系建立 (Relations)

### 3.1 双模式 UDF 对比矩阵

| 维度 | 嵌入式 Rust (`LANGUAGE rust`) | WASM (`LANGUAGE wasm`) |
|-----|------------------------------|------------------------|
| **执行位置** | 计算节点进程内 | 沙箱化 WASM 运行时 |
| **延迟** | < 1μs（标量函数） | 5-50μs（含序列化） |
| **隔离性** | 进程级（依赖 Rust 安全） | 沙箱级（内存+能力隔离） |
| **部署方式** | SQL 内联代码 | 预编译 WASM 模块 |
| **构建复杂度** | 低（单文件 SQL） | 中（需要 Cargo 构建链） |
| **生态兼容性** | RisingWave 专用 | 语言无关（Rust/C/Go） |
| **调试体验** | 受限（日志追踪） | 较好（wasmtime 调试） |
| **适用场景** | 简单转换、高频调用 | 复杂逻辑、多语言、安全敏感 |

### 3.2 RisingWave vs Flink UDF 架构映射

| 特性 | RisingWave Rust UDF | Flink Java/Scala UDF |
|-----|---------------------|---------------------|
| **语言运行时** | Rust（零 GC） | JVM（有 GC） |
| **执行模式** | 进程内嵌入 / WASM | JVM 类加载 |
| **标量函数** | `fn f(x: T) -> U` | `ScalarFunction.evaluate()` |
| **表函数** | `impl Iterator` | `TableFunction.collect()` |
| **聚合函数** | `#[aggregate]` 宏 | `AggregateFunction` 接口 |
| **类型系统** | SQL-Rust 映射 | SQL-Java 映射 |
| **状态访问** | 受限（只读参数） | 可通过 `RuntimeContext` 访问 |
| **向量化** | 自动（Arrow 格式） | 需显式实现 `Vectorized` |

### 3.3 类型系统关系图

```
SQL 类型层                    RisingWave 内部              Rust 类型层
┌─────────────┐              ┌─────────────┐              ┌─────────────┐
│   INTEGER   │─────────────→│    Int32    │←─────────────│    i32      │
├─────────────┤              ├─────────────┤              ├─────────────┤
│   BIGINT    │─────────────→│    Int64    │←─────────────│    i64      │
├─────────────┤              ├─────────────┤              ├─────────────┤
│   VARCHAR   │─────────────→│   Utf8      │←─────────────│   String    │
├─────────────┤              ├─────────────┤              ├─────────────┤
│  TIMESTAMP  │─────────────→│ Timestamp   │←─────────────│NaiveDateTime│
├─────────────┤              ├─────────────┤              ├─────────────┤
│  STRUCT<>   │─────────────→│ Struct      │←─────────────│ 自定义结构体 │
└─────────────┘              └─────────────┘              └─────────────┘
```

---

## 4. 论证过程 (Argumentation)

### 4.1 为什么选择 Rust 作为 UDF 语言？

**论证**: RisingWave 选择 Rust 作为主要 UDF 语言，基于以下技术权衡：

| 因素 | Rust 优势 | 对 RisingWave UDF 的意义 |
|-----|----------|------------------------|
| **内存安全** | 编译期所有权检查 | 防止 UDF 内存泄漏破坏数据库 |
| **零成本抽象** | 无运行时开销 | UDF 性能接近原生代码 |
| **FFI 友好** | 与 C ABI 兼容 | 易于与数据库内核集成 |
| **WASM 支持** | 原生 wasm32 目标 | 无缝支持 WASM UDF 模式 |
| **类型丰富** | 强大的类型系统 | 精确表达复杂数据结构 |

**与 Python UDF 对比**:

```
延迟对比 (标量函数):
┌─────────────────┬─────────────┬─────────────┐
│     场景        │  Rust UDF   │ Python UDF  │
├─────────────────┼─────────────┼─────────────┤
│ 简单整数加法     │   ~50ns     │   ~5μs      │
│ 字符串处理       │   ~200ns    │   ~20μs     │
│ JSON 解析       │   ~1μs      │   ~100μs    │
└─────────────────┴─────────────┴─────────────┘
```

### 4.2 嵌入式 vs WASM 模式选择决策树

```
UDF 开发需求分析
│
├─ 需要与其他语言互操作？
│  ├─ 是 → WASM 模式(支持多语言编译到 WASM)
│  └─ 否 → 继续评估
│
├─ 对延迟敏感 (< 100μs) 且高频调用？
│  ├─ 是 → 嵌入式 Rust 模式
│  └─ 否 → 继续评估
│
├─ 需要复杂依赖(外部 crate)？
│  ├─ 是 → WASM 模式(更灵活的构建链)
│  └─ 否 → 嵌入式模式(更简单)
│
├─ 安全隔离要求高(第三方 UDF)？
│  ├─ 是 → WASM 模式(沙箱隔离)
│  └─ 否 → 嵌入式模式(性能优先)
│
└─ 开发和调试便利性优先？
   ├─ 是 → WASM 模式(独立构建、测试)
   └─ 否 → 嵌入式模式(单文件部署)
```

---

## 5. 形式证明 / 工程论证

### Thm-RW-05: Rust UDF 类型安全定理

**定理**: RisingWave Rust UDF 的类型系统在编译期保证运行时类型安全，即：

**前提**:

1. SQL 函数声明类型为 $\tau_{sql} = (\tau_1, \tau_2, ..., \tau_n) \to \tau_{out}$
2. Rust 实现签名满足 $\Gamma \vdash f: \sigma(\tau_1) \times ... \times \sigma(\tau_n) \to \sigma(\tau_{out})$
3. 类型映射 $\sigma$ 是双射（Def-RW-20）

**结论**: 运行时不会发生类型相关的未定义行为：

$$
\forall e \in \text{Inputs}(\tau_{sql}): \text{Exec}(f, e) \in \text{Outputs}(\tau_{out}) \land \neg \text{UB}
$$

**证明**:

**步骤 1**（SQL 解析阶段）:
RisingWave 前端解析 `CREATE FUNCTION` 语句，验证类型名称合法性。

**步骤 2**（Rust 编译阶段）:
嵌入式 Rust 代码通过 `rustc` 编译，类型不匹配会在编译期报错。

**步骤 3**（边界检查）:
运行时，RisingWave 在调用 UDF 前验证输入值符合 SQL 类型约束（如非空检查）。

**步骤 4**（所有权系统）:
Rust 所有权系统保证 UDF 不会访问非法内存或产生数据竞争。

因此，类型安全在编译期和运行时双重保证 $\square$

---

### 5.2 WASM UDF 可移植性论证

**命题 (Prop-RW-17)**: WASM UDF 实现一次编译、多处运行的可移植性：

**论证**:

设 WASM 模块 $W$ 在平台 $P_1$ 上编译，对于任意符合 WASI 预览1 的运行时 $R$:

$$
\forall P_2 \in \text{Platforms}: \text{Exec}_R(W, P_2) = \text{Exec}_R(W, P_1)
$$

**工程实践**:

1. **架构无关**: wasm32 指令集与 x86/ARM 无关
2. **系统调用抽象**: WASI 提供 POSIX-like 可移植接口
3. **RisingWave 绑定**: Arrow UDF API 在不同平台行为一致

---

## 6. 实例验证 (Examples)

### 6.1 嵌入式 Rust 标量函数

**示例 1: 最大公约数 (GCD)**

```sql
CREATE FUNCTION gcd(x INT, y INT)
RETURNS INT
LANGUAGE rust
AS $$
    fn gcd(x: i32, y: i32) -> i32 {
        let mut a = x.abs();
        let mut b = y.abs();
        while b != 0 {
            let temp = b;
            b = a % b;
            a = temp;
        }
        a
    }
$$;

-- 使用
SELECT gcd(48, 18);  -- 结果: 6
```

**示例 2: 字符串相似度（编辑距离）**

```sql
CREATE FUNCTION edit_distance(s VARCHAR, t VARCHAR)
RETURNS INT
LANGUAGE rust
AS $$
    fn edit_distance(s: &str, t: &str) -> i32 {
        let s_chars: Vec<char> = s.chars().collect();
        let t_chars: Vec<char> = t.chars().collect();
        let m = s_chars.len();
        let n = t_chars.len();

        let mut dp = vec![vec![0; n + 1]; m + 1];

        for i in 0..=m {
            dp[i][0] = i;
        }
        for j in 0..=n {
            dp[0][j] = j;
        }

        for i in 1..=m {
            for j in 1..=n {
                let cost = if s_chars[i-1] == t_chars[j-1] { 0 } else { 1 };
                dp[i][j] = *[
                    dp[i-1][j] + 1,      // 删除
                    dp[i][j-1] + 1,      // 插入
                    dp[i-1][j-1] + cost  // 替换
                ].iter().min().unwrap();
            }
        }

        dp[m][n] as i32
    }
$$;

-- 使用
SELECT edit_distance('kitten', 'sitting');  -- 结果: 3
```

### 6.2 嵌入式 Rust 表函数

**示例 3: 生成整数序列**

```sql
CREATE FUNCTION series(n INT)
RETURNS TABLE (x INT)
LANGUAGE rust
AS $$
    fn series(n: i32) -> impl Iterator<Item = i32> {
        (1..=n).into_iter()
    }
$$;

-- 使用
SELECT * FROM series(5);
-- 结果: 1, 2, 3, 4, 5
```

**示例 4: 字符串分割（返回多行）**

```sql
CREATE FUNCTION split_text(input VARCHAR, delimiter VARCHAR)
RETURNS TABLE (part VARCHAR, idx INT)
LANGUAGE rust
AS $$
    fn split_text(input: &str, delimiter: &str) -> impl Iterator<Item = (String, i32)> + '_ {
        input.split(delimiter)
            .enumerate()
            .map(|(i, s)| (s.to_string(), i as i32))
    }
$$;

-- 使用
SELECT * FROM split_text('apple,banana,cherry', ',');
-- 结果:
-- part    | idx
-- --------|-----
-- apple   | 0
-- banana  | 1
-- cherry  | 2
```

### 6.3 结构化类型与 StructType

**示例 5: 返回复杂结构体**

```sql
-- 定义结构化类型
CREATE TYPE point AS (x DOUBLE, y DOUBLE);
CREATE TYPE circle AS (center point, radius DOUBLE);

-- 计算两个圆是否相交的 UDF
CREATE FUNCTION circles_intersect(c1 circle, c2 circle)
RETURNS BOOLEAN
LANGUAGE rust
AS $$
    use risingwave_udf::StructType;

    #[derive(StructType)]
    struct Point {
        x: f64,
        y: f64,
    }

    #[derive(StructType)]
    struct Circle {
        center: Point,
        radius: f64,
    }

    fn circles_intersect(c1: Circle, c2: Circle) -> bool {
        let dx = c1.center.x - c2.center.x;
        let dy = c1.center.y - c2.center.y;
        let distance = (dx * dx + dy * dy).sqrt();
        distance <= (c1.radius + c2.radius)
    }
$$;
```

### 6.4 WASM UDF 完整示例

**步骤 1: 创建 Rust 项目**

```bash
cargo new --lib risingwave_udf_example
cd risingwave_udf_example
```

**步骤 2: 配置 Cargo.toml**

```toml
[package]
name = "risingwave_udf_example"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
arrow-udf = "0.3"
chrono = { version = "0.4", features = ["wasmbind"] }
serde_json = "1.0"

[profile.release]
opt-level = 3
lto = true
```

**步骤 3: 实现 UDF（src/lib.rs）**

```rust
use arrow_udf::function;

/// 计算 Haversine 距离(地理坐标距离)
#[function("haversine(double, double, double, double) -> double")]
fn haversine(lat1: f64, lon1: f64, lat2: f64, lon2: f64) -> f64 {
    const R: f64 = 6371.0; // 地球半径(公里)

    let lat1_rad = lat1.to_radians();
    let lat2_rad = lat2.to_radians();
    let delta_lat = (lat2 - lat1).to_radians();
    let delta_lon = (lon2 - lon1).to_radians();

    let a = (delta_lat / 2.0).sin().powi(2)
        + lat1_rad.cos() * lat2_rad.cos() * (delta_lon / 2.0).sin().powi(2);
    let c = 2.0 * a.sqrt().atan2((1.0 - a).sqrt());

    R * c
}

/// JSON 字段提取(返回 JSONB)
#[function("json_extract(varchar, varchar) -> jsonb")]
fn json_extract(json_str: &str, path: &str) -> String {
    use serde_json::Value;

    let value: Value = serde_json::from_str(json_str).unwrap_or(Value::Null);

    // 简单路径解析: "user.name"
    let mut current = &value;
    for key in path.split('.') {
        current = current.get(key).unwrap_or(&Value::Null);
    }

    current.to_string()
}

/// 表函数:生成日期范围
#[function("date_range(timestamp, timestamp, interval) -> setof timestamp")]
fn date_range(start: chrono::NaiveDateTime, end: chrono::NaiveDateTime, step: chrono::Duration) -> impl Iterator<Item = chrono::NaiveDateTime> {
    std::iter::successors(Some(start), move |&prev| {
        let next = prev + step;
        if next <= end { Some(next) } else { None }
    })
}
```

**步骤 4: 编译为 WASM**

```bash
# 安装 wasm32-wasip1 目标
rustup target add wasm32-wasip1

# 编译发布版本
cargo build --target wasm32-wasip1 --release

# 生成 base64 编码(用于 SQL 嵌入)
base64 -w 0 target/wasm32-wasip1/release/risingwave_udf_example.wasm > udf.wasm.b64
```

**步骤 5: 在 RisingWave 中注册**

```sql
-- 方式 1: 直接嵌入 BASE64
CREATE FUNCTION haversine(DOUBLE, DOUBLE, DOUBLE, DOUBLE)
RETURNS DOUBLE
LANGUAGE wasm
AS '\x00asm...';  -- BASE64 编码的 WASM 字节码

-- 方式 2: 从文件系统链接(需 RisingWave 配置允许)
CREATE FUNCTION haversine(DOUBLE, DOUBLE, DOUBLE, DOUBLE)
RETURNS DOUBLE
LANGUAGE wasm
AS '/path/to/udf.wasm';

-- 使用 WASM UDF
SELECT
    store_name,
    haversine(user_lat, user_lon, store_lat, store_lon) AS distance_km
FROM user_locations, stores
WHERE haversine(user_lat, user_lon, store_lat, store_lon) < 10;
```

### 6.5 实时特征工程 UDF 案例

**场景**: 电商实时推荐系统的特征计算

```sql
-- 1. 创建用户行为源表
CREATE SOURCE user_behavior (
    user_id BIGINT,
    event_type VARCHAR,
    product_id BIGINT,
    price DECIMAL,
    event_time TIMESTAMP,
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    connector = 'kafka',
    topic = 'user_behavior',
    properties.bootstrap.server = 'kafka:9092'
) FORMAT PLAIN ENCODE JSON;

-- 2. 定义特征计算 UDF(嵌入式 Rust)
CREATE FUNCTION compute_user_features(
    prices ARRAY<DECIMAL>,
    categories ARRAY<VARCHAR>,
    timestamps ARRAY<TIMESTAMP>
) RETURNS STRUCT<
    avg_price DOUBLE,
    price_stddev DOUBLE,
    category_entropy DOUBLE,
    purchase_frequency_1h DOUBLE
>
LANGUAGE rust
AS $$
    use risingwave_udf::StructType;
    use std::collections::HashMap;

    #[derive(StructType)]
    struct UserFeatures {
        avg_price: f64,
        price_stddev: f64,
        category_entropy: f64,
        purchase_frequency_1h: f64,
    }

    fn compute_user_features(
        prices: Vec<rust_decimal::Decimal>,
        categories: Vec<String>,
        timestamps: Vec<chrono::NaiveDateTime>,
    ) -> UserFeatures {
        // 计算平均价格
        let price_f64: Vec<f64> = prices.iter()
            .map(|p| p.to_string().parse().unwrap_or(0.0))
            .collect();
        let avg_price = price_f64.iter().sum::<f64>() / price_f64.len() as f64;

        // 计算价格标准差
        let variance = price_f64.iter()
            .map(|p| (p - avg_price).powi(2))
            .sum::<f64>() / price_f64.len() as f64;
        let price_stddev = variance.sqrt();

        // 计算类别熵
        let mut cat_counts: HashMap<String, i32> = HashMap::new();
        for cat in &categories {
            *cat_counts.entry(cat.clone()).or_insert(0) += 1;
        }
        let total = categories.len() as f64;
        let category_entropy = -cat_counts.values()
            .map(|&c| {
                let p = c as f64 / total;
                p * p.log2()
            })
            .sum::<f64>();

        // 计算 1 小时购买频率
        let now = chrono::Local::now().naive_local();
        let count_1h = timestamps.iter()
            .filter(|&&t| (now - t).num_hours() < 1)
            .count() as f64;
        let purchase_frequency_1h = count_1h;

        UserFeatures {
            avg_price,
            price_stddev,
            category_entropy,
            purchase_frequency_1h,
        }
    }
$$;

-- 3. 创建特征物化视图
CREATE MATERIALIZED VIEW user_realtime_features AS
SELECT
    user_id,
    compute_user_features(
        ARRAY_AGG(price),
        ARRAY_AGG(category),
        ARRAY_AGG(event_time)
    ) AS features
FROM (
    SELECT
        user_id,
        price,
        SPLIT_PART(event_type, '_', 1) AS category,
        event_time
    FROM user_behavior
    WHERE event_time > NOW() - INTERVAL '24' HOUR
)
GROUP BY user_id;

-- 4. 查询特征
SELECT
    user_id,
    (features).avg_price,
    (features).category_entropy
FROM user_realtime_features
WHERE (features).purchase_frequency_1h > 5;
```

---

## 7. 可视化 (Visualizations)

### 7.1 RisingWave Rust UDF 双模式架构图

```mermaid
graph TB
    subgraph "SQL 查询层"
        SQL[SELECT udf(col) FROM ...]
    end

    subgraph "RisingWave Frontend"
        PLANNER[查询规划器]
        TYPE_CHECK[类型检查器]
    end

    subgraph "UDF 分发层"
        ROUTER{模式选择}
    end

    subgraph "嵌入式 Rust 模式"
        E_CODE[Rust 源码嵌入 SQL]
        E_COMPILE[rustc JIT 编译]
        E_EXEC[进程内执行
               < 1μs 延迟]
        E_CACHE[函数缓存]
    end

    subgraph "WASM 模式"
        W_CODE[Cargo 项目]
        W_BUILD[cargo build
                wasm32-wasip1]
        W_WASM[WASM 字节码]
        W_RUNTIME[WASM 运行时
                  Wasmtime]
        W_EXEC[沙箱执行
               5-50μs 延迟]
    end

    subgraph "数据层"
        ARROW[Arrow 列式格式]
        DATA[(数据分区)]
    end

    SQL --> PLANNER
    PLANNER --> TYPE_CHECK
    TYPE_CHECK --> ROUTER

    ROUTER -->|简单函数/低延迟| E_CODE
    ROUTER -->|复杂逻辑/多语言| W_WASM

    E_CODE --> E_COMPILE
    E_COMPILE --> E_EXEC
    E_EXEC --> E_CACHE

    W_WASM --> W_RUNTIME
    W_RUNTIME --> W_EXEC

    E_CACHE --> ARROW
    W_EXEC --> ARROW
    ARROW --> DATA
```

### 7.2 SQL-Rust 类型映射决策树

```mermaid
flowchart TD
    START[SQL 类型] --> Q1{数值类型?}

    Q1 -->|是| Q2{整数/浮点?}
    Q1 -->|否| Q3{字符串类型?}

    Q2 -->|整数| Q4{范围?}
    Q2 -->|浮点| Q5{精度?}

    Q4 -->|小| A1[i16]
    Q4 -->|中| A2[i32]
    Q4 -->|大| A3[i64]

    Q5 -->|单精度| A4[f32]
    Q5 -->|双精度| A5[f64]
    Q5 -->|精确小数| A6[rust_decimal::Decimal]

    Q3 -->|是| A7[String/&str]
    Q3 -->|否| Q6{时间类型?}

    Q6 -->|是| Q7{日期/时间/戳?}
    Q6 -->|否| Q8{复合类型?}

    Q7 -->|日期| A8[NaiveDate]
    Q7 -->|时间| A9[NaiveTime]
    Q7 -->|时间戳| A10[NaiveDateTime/DateTime]

    Q8 -->|数组| A11[Vec<T>]
    Q8 -->|结构体| A12[#[derive(StructType)]
    自定义结构体]
    Q8 -->|JSON| A13[serde_json::Value]
    Q8 -->|二进制| A14[Vec<u8>]
```

### 7.3 Flink → RisingWave UDF 迁移映射

```mermaid
graph LR
    subgraph "Flink Java UDF"
        F1[ScalarFunction]
        F2[TableFunction<T>]
        F3[AggregateFunction<T, ACC>]
        F4[AsyncFunction]
    end

    subgraph "迁移策略"
        S1[直接转换]
        S2[模式调整]
        S3[外部服务化]
    end

    subgraph "RisingWave Rust UDF"
        R1[fn f(x: T) -> U]
        R2[impl Iterator]
        R3[#[aggregate] 宏]
        R4[外部 API 调用]
    end

    F1 -->|简单计算| S1 --> R1
    F2 -->|返回多行| S1 --> R2
    F3 -->|聚合逻辑| S2 --> R3
    F4 -->|IO 操作| S3 --> R4
```

### 7.4 实时特征工程 UDF 数据流

```mermaid
sequenceDiagram
    participant Kafka as Kafka 数据源
    participant RW as RisingWave
    participant UDF as Rust UDF
    participant MV as 物化视图
    participant API as 推荐 API

    loop 实时数据流
        Kafka->>RW: 用户行为事件
        RW->>RW: 窗口聚合 (24h)
    end

    API->>RW: 查询用户特征
    RW->>UDF: 调用 compute_user_features
    UDF->>UDF: 计算统计特征
    UDF->>UDF: 计算熵/频率
    UDF-->>RW: 返回结构体
    RW->>MV: 增量更新
    MV-->>API: 返回特征向量

    Note over UDF: 延迟 < 1ms
    Note over MV: 实时物化
```

---

## 8. 引用参考 (References)









---

## 附录 A: 完整 SQL-Rust 类型映射参考

### A.1 标量类型映射

| SQL 类型 | Rust 类型 | 示例值 |
|---------|-----------|--------|
| `BOOLEAN` | `bool` | `true`, `false` |
| `SMALLINT` | `i16` | `42` |
| `INTEGER` | `i32` | `1000000` |
| `BIGINT` | `i64` | `9000000000` |
| `REAL` | `f32` | `3.14` |
| `DOUBLE` | `f64` | `3.14159265359` |
| `VARCHAR` | `String` / `&str` | `"hello"` |
| `BYTEA` | `Vec<u8>` / `&[u8]` | `vec![0x00, 0x01]` |
| `DATE` | `chrono::NaiveDate` | `2024-01-15` |
| `TIME` | `chrono::NaiveTime` | `14:30:00` |
| `TIMESTAMP` | `chrono::NaiveDateTime` | `2024-01-15 14:30:00` |
| `TIMESTAMPTZ` | `chrono::DateTime<chrono::Utc>` | `2024-01-15T14:30:00Z` |
| `DECIMAL` | `rust_decimal::Decimal` | `Decimal::new(12345, 2)` |
| `INTERVAL` | `chrono::Duration` | `Duration::hours(1)` |
| `JSONB` | `serde_json::Value` | `json!({"key": "value"})` |

### A.2 复合类型映射

| SQL 类型 | Rust 类型 | 说明 |
|---------|-----------|------|
| `ARRAY<T>` | `Vec<T>` | 动态大小数组 |
| `T[]` | `Vec<T>` | 数组字面量语法 |
| `STRUCT<a T1, b T2>` | `#[derive(StructType)] struct S { a: T1, b: T2 }` | 命名字段结构体 |
| `ROW(...)` | 元组或结构体 | 匿名结构体 |

### A.3 类型修饰符处理

| SQL 修饰符 | Rust 处理 |
|-----------|-----------|
| `NOT NULL` | 直接使用 Rust 类型 `T` |
| `NULL` | 使用 `Option<T>` |
| `ARRAY` | `Vec<T>` 或 `Vec<Option<T>>`（可空元素） |

---

## 附录 B: WASM UDF 构建完整脚本

### B.1 Makefile 模板

```makefile
# RisingWave WASM UDF 构建模板

WASM_TARGET = wasm32-wasip1
RELEASE_DIR = target/$(WASM_TARGET)/release
WASM_FILE = $(RELEASE_DIR)/udf.wasm
B64_FILE = udf.wasm.b64

.PHONY: all build install clean test

all: build

build:
 @echo "Building WASM module for $(WASM_TARGET)..."
 cargo build --target $(WASM_TARGET) --release
 @echo "Optimizing with wasm-opt..."
 wasm-opt -O3 $(WASM_FILE) -o $(WASM_FILE).opt
 mv $(WASM_FILE).opt $(WASM_FILE)
 @echo "Generating Base64..."
 base64 -w 0 $(WASM_FILE) > $(B64_FILE)
 @echo "Build complete: $(B64_FILE)"

install: build
 @echo "Generating SQL..."
 @echo "CREATE FUNCTION ... LANGUAGE wasm AS '\\x$$(cat $(B64_FILE))';" > install.sql

test:
 cargo test

clean:
 cargo clean
 rm -f $(B64_FILE) install.sql
```

### B.2 GitHub Actions CI/CD

```yaml
name: Build RisingWave UDF

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Install Rust
      uses: dtolnay/rust-action@stable
      with:
        targets: wasm32-wasip1

    - name: Install wasm-opt
      run: |
        wget https://github.com/WebAssembly/binaryen/releases/download/version_116/binaryen-version_116-x86_64-linux.tar.gz
        tar xzf binaryen-version_116-x86_64-linux.tar.gz
        sudo cp binaryen-version_116/bin/wasm-opt /usr/local/bin/

    - name: Build
      run: make build

    - name: Upload WASM
      uses: actions/upload-artifact@v3
      with:
        name: udf-wasm
        path: |
          *.wasm
          *.b64
```

---

## 附录 C: 故障排除

### C.1 常见错误与解决方案

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `type mismatch` | SQL-Rust 类型不匹配 | 检查 `Def-RW-20` 类型映射表 |
| `wasm module load failed` | WASM 模块不兼容 | 确认 `wasm32-wasip1` 目标 |
| `function not found` | 函数签名不匹配 | 检查 SQL 声明与 Rust 实现 |
| `memory access out of bounds` | WASM 内存溢出 | 增加 `memory.pages` 限制 |
| `chrono` 类型错误 | 时间类型不匹配 | 使用 `chrono::NaiveDateTime` |

### C.2 性能调试技巧

```sql
-- 查看 UDF 执行统计
EXPLAIN ANALYZE SELECT my_udf(column) FROM table;

-- 启用详细日志
SET udf_log_level = 'debug';
```

---

*文档状态: ✅ 已完成 (RW-UDF-01) | 字数统计: ~8000 字 | 代码示例: 15 个*
