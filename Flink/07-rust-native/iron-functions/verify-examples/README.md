# Iron Functions 验证示例

本目录包含可运行的 Rust UDF 示例，用于验证 Iron Functions 兼容性。

## 文件结构

```
verify-examples/
├── Cargo.toml          # Rust 项目配置
├── src/
│   └── lib.rs          # UDF 实现
├── examples/           # 使用示例(可选)
├── tests/              # 集成测试(可选)
└── README.md           # 本文件
```

## 快速开始

### 1. 环境准备

```bash
# 安装 Rust(如果尚未安装)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 安装 WASM 目标
rustup target add wasm32-unknown-unknown

# 验证安装
rustc --version
cargo --version
```

### 2. 编译 WASM 模块

```bash
# 在 verify-examples 目录下
cd Flink/14-rust-assembly-ecosystem/iron-functions/verify-examples

# 编译为 WASM
cargo build --release --target wasm32-unknown-unknown

# 验证输出
ls -la target/wasm32-unknown-unknown/release/*.wasm
```

### 3. 运行单元测试

```bash
cargo test
```

## 示例说明

### 示例 1: 字符串处理 (`process_string`)

支持操作：

- `upper` - 转大写
- `lower` - 转小写
- `reverse` - 反转
- `length` - 长度

输入格式：

```json
{
    "value": "hello",
    "operation": "upper"
}
```

### 示例 2: 数值计算 (`calculate`)

支持操作：

- `add` - 加法
- `subtract` - 减法
- `multiply` - 乘法
- `divide` - 除法
- `power` - 幂运算

输入格式：

```json
{
    "a": 10.0,
    "b": 5.0,
    "operation": "add"
}
```

### 示例 3: 数据验证 (`validate_data`)

验证：

- 邮箱格式
- 年龄范围

输入格式：

```json
{
    "email": "test@example.com",
    "age": 25
}
```

### 示例 4: JSON 处理 (`process_json`)

支持操作：

- `pretty` - 格式化输出
- `compact` - 紧凑输出
- `extract_keys` - 提取键名

输入格式：

```json
{
    "json_str": "{\"name\":\"test\"}",
    "operation": "pretty"
}
```

## 打包为 Flink UDF

使用 ironfun CLI 打包：

```bash
# 安装 ironfun(如果尚未安装)
curl -s https://irontools.dev/ironfun-cli-install.sh | sh

# 打包为 JAR
ironfun package-udf \
    --source-path . \
    --package-name com.demo.verify \
    --class-name VerifyExamples \
    --uber-jar
```

## 版本兼容性验证

运行版本检查脚本：

```bash
# 从项目根目录
python .scripts/iron-functions-tracker.py --check

# 更新版本记录
python .scripts/iron-functions-tracker.py --update
```

## 故障排除

### 编译错误

**错误**: `error: no such target: wasm32-unknown-unknown`

解决：

```bash
rustup target add wasm32-unknown-unknown
```

**错误**: `error: linking with cc failed`

解决（macOS）：

```bash
brew install llvm
```

### 运行时错误

**问题**: WASM 模块加载失败

检查：

1. 确认使用了 `crate-type = ["cdylib"]`
2. 确认使用了 `--release` 模式编译
3. 检查模块导出函数名是否正确

## 参考

- [Iron Functions 文档](https://irontools.dev/docs/)
- [Extism PDK 文档](https://extism.org/docs/write-a-plugin/rust-pdk/)
- [Flink 集成指南](../01-iron-functions-complete-guide.md)
