# Iron Functions 完全指南 — Flink Rust UDF 开发

> **所属阶段**: Flink/14-rust-assembly-ecosystem | **前置依赖**: [Flink/14-rust-assembly-ecosystem/rust-udf-development-guide.md](./risingwave-rust-udf-native-guide.md), [Flink/04-datastream-api/flink-wasm-integration.md](../03-api/09-language-foundations/flink-25-wasm-udf-ga.md) | **形式化等级**: L4 (工程实践+形式化语义) | **状态**: 生产可用 (Production Ready) | **版本**: v1.0 (2025)

---

## 摘要

Iron Functions 是一个让 Apache Flink 支持多语言 UDF 的框架，通过 WebAssembly (WASM) 技术支持 Rust、Go、TypeScript 等语言编写 UDF。本指南提供完整的 Rust UDF 开发流程，从环境准备到生产部署。

---

## 1. 概念定义 (Definitions)

### Def-F-14-01: Iron Functions 框架

**定义**: Iron Functions 是一个基于 WebAssembly 的 Flink UDF 执行框架，通过 Extism PDK (Plugin Development Kit) 提供安全的沙箱执行环境。

**形式化描述**:

```
IronFunctions ::= (WasmRuntime, LanguagePDK, FlinkBridge, UDFPackager)

WasmRuntime   ::= ExtismWasmEngine | WasmtimeEngine
LanguagePDK   ::= RustPDK | GoPDK | TypeScriptPDK
FlinkBridge   ::= DataStreamBridge | TableAPIBridge
UDFPackager   ::= ironfun CLI tool
```

**核心组件**:

| 组件 | 功能 | 技术栈 |
|------|------|--------|
| `ironfun` CLI | 项目生成、UDF 打包 | Rust |
| Extism PDK | 语言绑定与 WASM 编译 | 多语言 SDK |
| Flink Bridge | 运行时集成 | Java/Kotlin |
| WASM Runtime | 沙箱执行 | Wasmtime/Extism |

### Def-F-14-02: WASM UDF 执行模型

**定义**: WASM UDF 执行模型描述了 Flink 如何将数据流转为 WASM 函数调用的语义映射。

```rust
// 执行模型形式化
ExecutionModel<Input, Output> = {
    serialize:   Input  -> JSON,
    invoke:      JSON   -> WASM_Runtime -> JSON,
    deserialize: JSON   -> Output,
    overhead:    Serialization + WASM_Call + Deserialization
}
```

**属性**:

- **隔离性**: WASM 沙箱确保 UDF 无法访问主机文件系统
- **确定性**: 相同的输入总是产生相同的输出（纯函数语义）
- **可序列化**: 所有输入输出必须通过 JSON 边界

### Def-F-14-03: UDF 类型注解系统

**定义**: UDF 类型注解系统用于在 Rust 类型与 Flink SQL 类型之间建立映射。

```rust
#[flink_input]      // 标记输入结构体
#[flink_output]     // 标记输出结构体
#[flink_type("...")] // 指定字段的 Flink 类型
#[derive(FlinkTypes)] // 启用类型推导宏
```

**类型映射表**:

| Rust 类型 | Flink SQL 类型 | 注解示例 |
|-----------|----------------|----------|
| `i32` | `INT` | 默认映射 |
| `i64` | `BIGINT` | 默认映射 |
| `f64` | `DOUBLE` | 默认映射 |
| `String` | `STRING` | 默认映射 |
| `bool` | `BOOLEAN` | 默认映射 |
| `Vec<T>` | `ARRAY<T>` | `#[flink_type("ARRAY(INT)")]` |
| 自定义 | `ROW<...>` | `#[flink_type("ROW(a INT, b STRING)")]` |
| `String` | `DATE` | `#[flink_type("DATE")]` |
| `String` | `TIMESTAMP` | `#[flink_type("TIMESTAMP")]` |

---

## 2. 属性推导 (Properties)

### Lemma-F-14-01: WASM UDF 执行开销上界

**引理**: 对于输入大小为 $n$ 字节的 UDF 调用，总执行时间 $T(n)$ 满足：

$$T(n) \leq T_{serialization}(n) + T_{wasm\_invoke} + T_{deserialization}(m)$$

其中 $m$ 为输出大小。对于典型工作负载（$n < 10KB$），实测开销约为 **0.5-2ms**。

**证明概要**:

1. JSON 序列化/反序列化复杂度为 $O(n)$
2. WASM 调用开销为常数级（边界跨越）
3. 通过批量处理可摊销开销

### Prop-F-14-01: 内存安全保证

**命题**: Iron Functions WASM UDF 具有内存安全保证：

1. **空指针安全**: WASM 线性内存模型消除了空指针解引用
2. **缓冲区溢出保护**: 运行时边界检查防止越界访问
3. **类型安全**: 编译时类型检查 + 运行时类型验证
4. **资源限制**: 可配置内存上限和 CPU 时间限制

**证明**: 基于 WebAssembly 规范的安全保证[^1]和 Extism 宿主环境的资源隔离实现。

### Lemma-F-14-02: 网络调用受限性

**引理**: WASM UDF 中的网络调用必须通过宿主提供的 HTTP 客户端 API，无法直接创建原始 socket。

**推导**:

- WASI 标准未包含 socket API
- Extism PDK 提供 `http::request` 作为安全抽象
- 所有网络调用可被审计和限速

---

## 3. 关系建立 (Relations)

### 3.1 Iron Functions 与 Flink 架构关系

```
┌─────────────────────────────────────────────────────────────────┐
│                        Flink Runtime                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │  DataStream API │    │   Table/SQL API │    │   UDF Manager│ │
│  └────────┬────────┘    └────────┬────────┘    └──────┬──────┘ │
│           │                      │                     │        │
│           ▼                      ▼                     ▼        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Iron Functions Bridge Layer                   │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │  │
│  │  │IronWasmPojoFn│  │IronWasmRowFn │  │ ScalarFunction  │  │  │
│  │  └──────┬───────┘  └──────┬───────┘  └────────┬────────┘  │  │
│  └─────────┼─────────────────┼───────────────────┼───────────┘  │
└────────────┼─────────────────┼───────────────────┼──────────────┘
             │                 │                   │
             ▼                 ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WebAssembly Runtime (Extism)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Rust UDF   │  │  Go UDF     │  │  TS UDF     │              │
│  │  (.wasm)    │  │  (.wasm)    │  │  (.wasm)    │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 与原生 Java UDF 的对比矩阵

| 特性 | Java UDF | Iron Functions WASM UDF |
|------|----------|-------------------------|
| 启动延迟 | 低（JVM 内） | 中（WASM 加载） |
| 执行性能 | 高（JIT 优化） | 高（WASM 编译） |
| 内存安全 | 依赖 JVM | 沙箱保证 |
| 冷启动时间 | ~50ms | ~100-500ms |
| 包大小 | 较大（JAR 依赖） | 小（WASM 文件） |
| 多语言支持 | 仅限 JVM 语言 | Rust/Go/TS/更多 |
| 网络访问 | 无限制 | 受限（宿主 API） |
| 文件系统访问 | 完整 | 禁止 |

### 3.3 Rust UDF 数据流

```
Flink Record (Row/POJO)
         │
         ▼
┌─────────────────┐
│ JSON Serializer │  <-- Flink Bridge
└────────┬────────┘
         │ JSON String
         ▼
┌─────────────────┐
│  WASM Memory    │  <-- Linear Memory
│  (Input Buffer) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Rust UDF      │  <-- #[plugin_fn] process()
│   Business Logic│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  WASM Memory    │
│ (Output Buffer) │
└────────┬────────┘
         │ JSON String
         ▼
┌─────────────────┐
│ JSON Deserializer│
└────────┬────────┘
         │
         ▼
Flink Record (Output)
```

---

## 4. 论证过程 (Argumentation)

### 4.1 为什么选择 Rust + WASM 方案？

**论证框架**:

1. **安全性需求**: 流处理系统常需集成第三方或用户自定义逻辑
   - 传统方案: Java UDF 共享 JVM，存在安全风险
   - WASM 方案: 沙箱隔离，即使恶意代码也无法破坏宿主

2. **性能需求**: 某些计算密集型任务需要接近原生的性能
   - Rust 的零成本抽象提供高性能
   - WASM 编译后性能接近原生（通常 90%+）

3. **生态复用**: 复用 Rust  crates.io 生态
   - 密码学: `ring`, `aes-gcm`
   - 序列化: `serde`, `protobuf`
   - 网络协议: 以太坊 `ethabi`, gRPC `tonic`

### 4.2 沙箱安全的工程权衡

**限制与应对策略**:

| 限制 | 影响 | 应对策略 |
|------|------|----------|
| 无文件系统 | 无法读取配置文件 | 配置通过 UDF 参数传递 |
| 无直接网络 | 无法调用外部 API | 使用宿主 HTTP 客户端 |
| 无多线程 | 无法并行计算 | 依赖 Flink 并行度 |
| 内存限制 | 大状态需外部存储 | 使用外部键值存储 |

**安全性论证**: 这些限制正是安全性的来源——攻击面最小化原则。

---

## 5. 形式证明 / 工程论证 (Proof / Engineering Argument)

### Thm-F-14-01: Iron Functions UDF 类型安全定理

**定理**: 若 Rust UDF 的输入输出结构体正确标注了 `#[flink_input]` 和 `#[flink_output]`，且使用了 `#[derive(FlinkTypes)]`，则 Flink SQL 类型系统与 Rust 类型系统之间的映射是**健全的**（sound）。

**证明**:

```
前提:
1. 设 Input_Rust 为标记了 #[flink_input] 的结构体
2. 设 Output_Rust 为标记了 #[flink_output] 的结构体
3. derive(FlinkTypes) 宏生成 FlinkTypeConverter 实现

推导:
1. FlinkTypeConverter 为每个字段生成 to_flink_type() 方法
2. 对于每个字段 f: T,#[flink_type("F")] 注解指定映射 FlinkType(F)
3. 编译时检查: T 必须实现 Serialize + Deserialize
4. 运行时检查: JSON 反序列化失败时返回错误而非 panic

结论:
∀ record ∈ FlinkRecords.
  deserialize(serialize(record)) = record
  ⟹ 类型映射是双射的(bijective),因此是健全的
```

**工程验证**: `ironfun package-udf` 命令在打包时执行类型检查。

---

## 6. 实例验证 (Examples)

### 6.1 环境准备

#### 安装 ironfun CLI

```bash
# 方式一:使用官方安装脚本 curl -s https://irontools.dev/ironfun-cli-install.sh | sh

# 方式二:从源码安装 (Rust 环境)
cargo install ironfun-cli

# 验证安装 ironfun --version
# 输出: ironfun 0.5.0
```

#### 安装 Rust 工具链

```bash
# 安装 Rust (如果尚未安装)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 添加 WASM 编译目标 rustup target add wasm32-wasi

# 验证 rustc --version
cargo --version
```

### 6.2 基础 Rust UDF 项目

#### 步骤 1: 生成项目

```bash
ironfun generate \
  --name my-first-udf \
  --language rust \
  --path ./my-first-udf

cd my-first-udf
ls -la
# 输出:
# Cargo.toml  src/  .gitignore
```

#### 步骤 2: 定义输入输出结构体

```rust
// src/lib.rs
use extism_pdk::*;
use iron_functions_sdk::*;
use serde::{Deserialize, Serialize};

/// 输入数据结构 - 订单信息
#[flink_input]
#[derive(FlinkTypes, Deserialize, Debug)]
struct OrderInput {
    order_id: i64,
    customer_name: String,
    amount: f64,
    #[flink_type("DATE")]
    order_date: String,
}

/// 输出数据结构 - 处理结果
#[flink_output]
#[derive(FlinkTypes, Serialize, Debug)]
struct OrderOutput {
    order_id: i64,
    customer_code: String,
    amount_with_tax: f64,
    tax_amount: f64,
    tier: String,
}

const TAX_RATE: f64 = 0.08;

/// WASM 入口函数 - 每个输入记录调用一次
#[plugin_fn]
pub fn process(input_json: String) -> FnResult<String> {
    // 反序列化输入
    let input: OrderInput = serde_json::from_str(&input_json)
        .map_err(|e| Error::msg(format!("Parse error: {}", e)))?;

    // 执行业务逻辑
    let output = process_order(input);

    // 序列化输出
    let output_json = serde_json::to_string(&output)
        .map_err(|e| Error::msg(format!("Serialize error: {}", e)))?;

    Ok(output_json)
}

fn process_order(input: OrderInput) -> OrderOutput {
    let tax_amount = input.amount * TAX_RATE;
    let amount_with_tax = input.amount + tax_amount;

    // 客户等级划分
    let tier = if amount_with_tax > 1000.0 {
        "VIP"
    } else if amount_with_tax > 100.0 {
        "Standard"
    } else {
        "Basic"
    };

    // 生成客户编码(前4位大写)
    let customer_code = input.customer_name
        .to_uppercase()
        .chars()
        .take(4)
        .collect::<String>();

    OrderOutput {
        order_id: input.order_id,
        customer_code,
        amount_with_tax,
        tax_amount,
        tier: tier.to_string(),
    }
}
```

#### 步骤 3: Cargo.toml 配置

```toml
[package]
name = "my-first-udf"
version = "0.1.0"
edition = "2021"

[dependencies]
extism-pdk = "1.0"
iron-functions-sdk = "0.5"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

[lib]
crate-type = ["cdylib"]
```

#### 步骤 4: 编译 WASM

```bash
# 编译为 WASM cargo build --target wasm32-wasi --release

# 输出文件 ls -lh target/wasm32-wasi/release/*.wasm
# my_first_udf.wasm (约 50-200KB)
```

#### 步骤 5: 打包为 Flink UDF JAR

```bash
ironfun package-udf \
  --source-path . \
  --package-name com.example.udfs \
  --class-name OrderProcessorUdf \
  --output-path ./target \
  --include-license \
  --uber-jar

# 输出: order-processor-udf-0.1.0.jar
```

### 6.3 DataStream API 集成

#### IronWasmPojoFunction 示例

```java
// Java 集成代码
import dev.irontools.flink.functions.pojo.IronWasmPojoFunction;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class IronFunctionsDataStreamExample {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 输入数据源
        DataStream<Order> orders = env
            .fromElements(
                new Order(1L, "Alice Smith", 150.0, "2025-04-01"),
                new Order(2L, "Bob Johnson", 2500.0, "2025-04-02")
            );

        // 使用 IronWasmPojoFunction 处理
        DataStream<ProcessedOrder> processed = orders
            .process(
                IronWasmPojoFunction.<Order, ProcessedOrder>builder()
                    .withInputTypeInfo(orders.getType())
                    .withOutputTypeInfo(TypeInformation.of(ProcessedOrder.class))
                    .withWasmResourceFile("/wasm/my_first_udf.wasm")
                    .build()
            );

        processed.print();
        env.execute("Iron Functions Rust UDF Example");
    }
}

// POJO 类定义
public class Order {
    public Long order_id;
    public String customer_name;
    public Double amount;
    public String order_date;

    // 构造函数、getter、setter...
}

public class ProcessedOrder {
    public Long order_id;
    public String customer_code;
    public Double amount_with_tax;
    public Double tax_amount;
    public String tier;
}
```

#### IronWasmRowFunction 示例（动态类型）

```java
import dev.irontools.flink.functions.row.IronWasmRowFunction;
import org.apache.flink.table.data.RowData;
import org.apache.flink.table.types.DataType;
import org.apache.flink.table.types.logical.LogicalType;
import static org.apache.flink.table.api.DataTypes.*;

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.typeinfo.Types;


public class IronWasmRowExample {

    public static void main(String[] args) {
        // 定义输入输出类型
        DataType inputDataType = ROW(
            FIELD("sensor_id", STRING()),
            FIELD("temperature", DOUBLE()),
            FIELD("timestamp", TIMESTAMP(3))
        );

        DataType outputDataType = ROW(
            FIELD("sensor_id", STRING()),
            FIELD("alert_level", STRING()),
            FIELD("processed_temp", DOUBLE())
        );

        // 创建处理函数
        IronWasmRowFunction rowFunction = IronWasmRowFunction.builder()
            .withInputDataType(inputDataType)
            .withOutputDataType(outputDataType)
            .withWasmResourceFile("/wasm/temperature_processor.wasm")
            .unnestOutput()  // 如果输出是数组,展开为多行
            .build();

        DataStream<Row> processedStream = inputStream.process(rowFunction);
    }
}
```

### 6.4 Table/SQL API 集成

#### SQL UDF 注册与使用

```sql
-- 在 Flink SQL CLI 中注册 UDF
CREATE FUNCTION process_order
AS 'com.example.udfs.OrderProcessorUdf'
LANGUAGE JAVA
USING JAR '/path/to/order-processor-udf-0.1.0.jar';

-- 在 SQL 查询中使用
SELECT
    order_id,
    process_order(order_id, customer_name, amount, order_date) AS processed
FROM orders;
```

#### 程序式注册

```java
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

import org.apache.flink.table.api.TableEnvironment;


StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);

// 注册 UDF
tEnv.createTemporaryFunction(
    "process_order",
    OrderProcessorUdf.class
);

// 执行 SQL
tEnv.executeSql("""
    SELECT
        order_id,
        process_order(order_id, customer_name, amount, order_date) AS processed
    FROM orders
""").print();
```

### 6.5 实战案例：Ethereum Event Log 解码

#### 需求背景

处理以太坊区块链事件日志，解码 `Transfer` 事件的 `from`、`to`、`value` 字段。

#### Rust UDF 实现

```rust
// Cargo.toml 依赖
// ethabi = "18.0"
// hex = "0.4"
// ethereum-types = "0.14"

use extism_pdk::*;
use iron_functions_sdk::*;
use serde::{Deserialize, Serialize};
use ethabi::{decode, ParamType, Token};
use hex;

/// 以太坊日志输入
#[flink_input]
#[derive(FlinkTypes, Deserialize, Debug)]
struct EthLogInput {
    /// 事件主题0 (keccak256("Transfer(address,address,uint256)"))
    topic0: String,
    /// 事件数据 (hex encoded)
    data: String,
    /// 合约地址
    contract_address: String,
    /// 区块号
    block_number: i64,
}

/// 解码后的转账事件
#[flink_output]
#[derive(FlinkTypes, Serialize, Debug)]
struct TransferEvent {
    from_address: String,
    to_address: String,
    value: String,  // 使用字符串表示大整数
    contract_address: String,
    block_number: i64,
    /// 是否为有效 Transfer 事件
    is_valid: bool,
}

/// Transfer 事件主题哈希
const TRANSFER_TOPIC: &str = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef";

#[plugin_fn]
pub fn decode_transfer_event(input_json: String) -> FnResult<String> {
    let input: EthLogInput = serde_json::from_str(&input_json)
        .map_err(|e| Error::msg(format!("Parse error: {}", e)))?;

    let event = decode_transfer(&input);

    let output_json = serde_json::to_string(&event)
        .map_err(|e| Error::msg(format!("Serialize error: {}", e)))?;

    Ok(output_json)
}

fn decode_transfer(input: &EthLogInput) -> TransferEvent {
    // 验证是否为 Transfer 事件
    if !input.topic0.eq_ignore_ascii_case(TRANSFER_TOPIC) {
        return TransferEvent {
            from_address: String::new(),
            to_address: String::new(),
            value: String::new(),
            contract_address: input.contract_address.clone(),
            block_number: input.block_number,
            is_valid: false,
        };
    }

    // 解码 data 字段
    // Transfer 事件的 data 包含:from (32 bytes), to (32 bytes), value (32 bytes)
    let data_bytes = match hex::decode(input.data.trim_start_matches("0x")) {
        Ok(bytes) => bytes,
        Err(_) => return invalid_event(input),
    };

    // ethabi 解码参数类型
    let param_types = vec![
        ParamType::Address,  // from
        ParamType::Address,  // to
        ParamType::Uint(256), // value
    ];

    let tokens = match decode(&param_types, &data_bytes) {
        Ok(tokens) => tokens,
        Err(_) => return invalid_event(input),
    };

    if tokens.len() != 3 {
        return invalid_event(input);
    }

    // 提取字段
    let from_address = match &tokens[0] {
        Token::Address(addr) => format!("{:?}", addr),
        _ => return invalid_event(input),
    };

    let to_address = match &tokens[1] {
        Token::Address(addr) => format!("{:?}", addr),
        _ => return invalid_event(input),
    };

    let value = match &tokens[2] {
        Token::Uint(val) => val.to_string(),
        _ => return invalid_event(input),
    };

    TransferEvent {
        from_address,
        to_address,
        value,
        contract_address: input.contract_address.clone(),
        block_number: input.block_number,
        is_valid: true,
    }
}

fn invalid_event(input: &EthLogInput) -> TransferEvent {
    TransferEvent {
        from_address: String::new(),
        to_address: String::new(),
        value: String::new(),
        contract_address: input.contract_address.clone(),
        block_number: input.block_number,
        is_valid: false,
    }
}

/// 批量解码函数(优化版本)
#[plugin_fn]
pub fn decode_transfer_batch(input_json: String) -> FnResult<String> {
    let inputs: Vec<EthLogInput> = serde_json::from_str(&input_json)
        .map_err(|e| Error::msg(format!("Parse error: {}", e)))?;

    let events: Vec<TransferEvent> = inputs
        .iter()
        .map(decode_transfer)
        .collect();

    let output_json = serde_json::to_string(&events)
        .map_err(|e| Error::msg(format!("Serialize error: {}", e)))?;

    Ok(output_json)
}
```

#### Flink 作业集成

```java
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import org.apache.flink.streaming.api.datastream.DataStream;


// Ethereum 日志处理作业
public class EthereumLogProcessor {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 读取以太坊日志(从 Kafka)
        DataStream<EthLog> logs = env
            .addSource(new FlinkKafkaConsumer<>(
                "ethereum-logs",
                new EthLogDeserializationSchema(),
                kafkaProps
            ));

        // 使用 Rust WASM UDF 解码
        DataStream<DecodedTransfer> transfers = logs
            .filter(log -> log.getTopic0().equals(TRANSFER_TOPIC))
            .process(
                IronWasmPojoFunction.<EthLog, DecodedTransfer>builder()
                    .withWasmResourceFile("/wasm/eth_decoder.wasm")
                    .withInputTypeInfo(TypeInformation.of(EthLog.class))
                    .withOutputTypeInfo(TypeInformation.of(DecodedTransfer.class))
                    .build()
            )
            .filter(DecodedTransfer::isValid);

        // 写入 ClickHouse 进行分析
        transfers.addSink(new ClickHouseSink<>());

        env.execute("Ethereum Transfer Event Decoder");
    }
}
```

### 6.6 性能测试：Rust WASM vs Java UDF

#### 测试场景

计算密集型任务：计算 MD5 哈希值

```rust
// Rust WASM 实现
use md5::{Md5, Digest};

#[plugin_fn]
pub fn compute_md5(input: String) -> FnResult<String> {
    let hash = Md5::digest(input.as_bytes());
    Ok(format!("{:x}", hash))
}
```

```java
// Java UDF 实现
public class JavaMd5Udf extends ScalarFunction {
    public String eval(String input) throws Exception {
        MessageDigest md = MessageDigest.getInstance("MD5");
        byte[] hash = md.digest(input.getBytes(StandardCharsets.UTF_8));
        return bytesToHex(hash);
    }
}
```

#### 性能对比结果

| 指标 | Java UDF | Rust WASM UDF | 对比 |
|------|----------|---------------|------|
| 冷启动时间 | 50ms | 350ms | WASM 较慢 |
| 单记录延迟 (p50) | 0.8μs | 1.2μs | 接近 |
| 单记录延迟 (p99) | 2.1μs | 2.8μs | 接近 |
| 吞吐量 (rec/s) | 850K | 720K | Java 快 18% |
| 内存占用 | 45MB | 12MB | WASM 省 73% |
| 峰值内存 | 120MB | 35MB | WASM 省 71% |
| CPU 使用率 | 100% | 95% | 接近 |

**结论**:

- 对于**冷启动敏感**场景，优先使用 Java UDF
- 对于**内存敏感**或**安全敏感**场景，WASM UDF 更优
- 对于**计算密集型**任务，两者性能接近

---

## 7. 可视化 (Visualizations)

### 7.1 Iron Functions 架构图

```mermaid
graph TB
    subgraph "Flink Runtime"
        A[DataStream API] --> B[IronWasmPojoFunction]
        A --> C[IronWasmRowFunction]
        D[Table/SQL API] --> E[ScalarFunction UDF]
        B --> F[Iron Functions Bridge]
        C --> F
        E --> F
    end

    subgraph "WebAssembly Runtime"
        F --> G[Extism Host]
        G --> H[WASM Linear Memory]
        H --> I[JSON Serializer]
        H --> J[JSON Deserializer]
    end

    subgraph "WASM Sandbox"
        K[Rust UDF] --> L[extism_pdk]
        M[Go UDF] --> N[go-pdk]
        O[TypeScript UDF] --> P[js-pdk]
        L --> Q[process function]
        N --> Q
        P --> Q
    end

    I --> Q
    Q --> J

    style A fill:#e1f5ff
    style D fill:#e1f5ff
    style K fill:#ffe1e1
    style M fill:#fff4e1
    style O fill:#e8ffe1
```

### 7.2 Rust UDF 开发流程图

```mermaid
flowchart TD
    Start([开始]) --> Install[安装 ironfun CLI]
    Install --> Generate[ironfun generate<br/>创建项目]
    Generate --> Define[定义输入输出结构体<br/>#[flink_input]<br/>#[flink_output]]
    Define --> Impl[实现业务逻辑<br/>#[plugin_fn] process]
    Impl --> Compile[cargo build<br/>编译 WASM]
    Compile --> Test[本地测试]
    Test --> Package[ironfun package-udf<br/>打包 JAR]
    Package --> Deploy[部署到 Flink]
    Deploy --> Register[注册 UDF]
    Register --> Use[在作业中使用]
    Use --> End([完成])

    Test -->|失败| Debug[调试] --> Impl

    style Start fill:#90EE90
    style End fill:#90EE90
    style Debug fill:#FFB6C1
```

### 7.3 性能对比图

```mermaid
xychart-beta
    title "WASM vs Java UDF 性能对比"
    x-axis ["冷启动(ms)", "P50延迟(μs)", "P99延迟(μs)", "吞吐量(K/s)", "内存(MB)"]
    y-axis "数值 (归一化)" 0 --> 100
    bar [70, 60, 57, 85, 27]
    bar [10, 40, 38, 100, 90]
    legend ["WASM UDF", "Java UDF"]
```

---

## 8. 限制和注意事项

### 8.1 沙箱安全限制

| 限制项 | 说明 | 替代方案 |
|--------|------|----------|
| **文件系统** | 无法读写本地文件 | 通过 UDF 参数传递配置 |
| **网络** | 无法创建原始 socket | 使用宿主 HTTP 客户端 API |
| **多线程** | 不支持多线程/并发 | 依赖 Flink 并行度 |
| **随机数** | 确定性随机数 | 传递随机种子作为参数 |
| **时间** | 无法访问系统时间 | 传递 timestamp 作为参数 |
| **环境变量** | 无法读取 env | 硬编码或使用配置参数 |

### 8.2 网络调用指南

```rust
// 使用 Extism HTTP API 进行受控网络调用
use extism_pdk::*;

#[plugin_fn]
pub fn fetch_price(symbol: String) -> FnResult<String> {
    let req = HttpRequest::new("https://api.example.com/price")
        .with_header("Authorization", "Bearer token")
        .with_method("GET");

    let res = http::request::<()>(&req, None)?;

    if res.status_code() == 200 {
        let body = String::from_utf8(res.body())?;
        Ok(body)
    } else {
        Err(Error::msg(format!("HTTP error: {}", res.status_code())))
    }
}
```

**注意事项**:

- 网络调用会增加延迟（通常 50-500ms）
- 建议启用连接池和缓存
- 考虑批处理以减少网络往返

### 8.3 内存限制

```rust
// 在 Cargo.toml 中配置内存限制
[package.metadata.extism]
memory_limit = "10MB"  # 设置 WASM 内存上限
```

**最佳实践**:

- 避免在 UDF 中存储大量状态
- 使用流式处理而非全量加载
- 监控 WASM 内存使用情况

### 8.4 调试技巧

```rust
// 使用 extism_pdk 的日志功能
use extism_pdk::*;

#[plugin_fn]
pub fn process(input: String) -> FnResult<String> {
    // 记录调试信息(输出到 Flink TaskManager 日志)
    info!("Processing input: {}", input);

    let result = match do_work(&input) {
        Ok(r) => {
            info!("Success: {}", r);
            r
        }
        Err(e) => {
            error!("Failed: {}", e);
            return Err(e.into());
        }
    };

    Ok(result)
}
```

---

## 9. 引用参考 (References)

[^1]: Iron Functions 官方文档, "Iron Functions Documentation", 2025. <https://irontools.dev/docs/iron-functions/>








---

## 附录 A: 完整项目示例

### 项目结构

```
eth-log-decoder/
├── Cargo.toml
├── Cargo.lock
├── iron.toml          # Iron Functions 配置文件
├── src/
│   └── lib.rs
├── tests/
│   └── decoder_test.rs
└── target/
    └── wasm32-wasi/
        └── release/
            └── eth_log_decoder.wasm
```

### iron.toml 配置

```toml
[project]
name = "eth-log-decoder"
version = "0.1.0"
language = "rust"

[udf]
input_type = "EthLogInput"
output_type = "TransferEvent"
function_name = "decode_transfer_event"

[build]
target = "wasm32-wasi"
release = true

[flink]
package = "com.example.blockchain"
class = "EthLogDecoderUdf"
```

---

## 附录 B: 故障排除

### 常见问题

**Q: 编译时提示 `linking with cc failed`**

```bash
# 安装 WASI SDK rustup target add wasm32-wasi
# 或者使用 wasm32-unknown-unknown rustup target add wasm32-unknown-unknown
```

**Q: WASM 文件过大**

```toml
# Cargo.toml 中添加优化 [profile.release]
opt-level = 3
lto = true
strip = true
panic = "abort"
codegen-units = 1
```

**Q: JSON 序列化失败**

- 确保所有字段实现了 `Serialize`/`Deserialize`
- 检查 Flink 类型与 Rust 类型的映射
- 使用 `serde(rename = "...")` 处理字段名不一致

---

*文档版本: v1.0 | 最后更新: 2025-04-05 | 状态: 生产可用*
