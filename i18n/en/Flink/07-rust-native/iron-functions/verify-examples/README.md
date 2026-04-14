---
title: "Iron Functions Verification Examples"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Iron Functions Verification Examples

This directory contains runnable Rust UDF examples for verifying Iron Functions compatibility.

## File Structure

```
verify-examples/
├── Cargo.toml          # Rust project configuration
├── src/
│   └── lib.rs          # UDF implementation
├── examples/           # Usage examples (optional)
├── tests/              # Integration tests (optional)
└── README.md           # This file
```

## Quick Start

### 1. Environment Setup

```bash
# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install WASM target
rustup target add wasm32-unknown-unknown

# Verify installation
rustc --version
cargo --version
```

### 2. Compile WASM Module

```bash
# In the verify-examples directory
cd Flink/14-rust-assembly-ecosystem/iron-functions/verify-examples

# Compile to WASM
cargo build --release --target wasm32-unknown-unknown

# Verify output
ls -la target/wasm32-unknown-unknown/release/*.wasm
```

### 3. Run Unit Tests

```bash
cargo test
```

## Example Descriptions

### Example 1: String Processing (`process_string`)

Supported operations:

- `upper` - Convert to uppercase
- `lower` - Convert to lowercase
- `reverse` - Reverse string
- `length` - Get length

Input format:

```json
{
    "value": "hello",
    "operation": "upper"
}
```

### Example 2: Numeric Computation (`calculate`)

Supported operations:

- `add` - Addition
- `subtract` - Subtraction
- `multiply` - Multiplication
- `divide` - Division
- `power` - Power

Input format:

```json
{
    "a": 10.0,
    "b": 5.0,
    "operation": "add"
}
```

### Example 3: Data Validation (`validate_data`)

Validations:

- Email format
- Age range

Input format:

```json
{
    "email": "test@example.com",
    "age": 25
}
```

### Example 4: JSON Processing (`process_json`)

Supported operations:

- `pretty` - Pretty print
- `compact` - Compact output
- `extract_keys` - Extract keys

Input format:

```json
{
    "json_str": "{\"name\":\"test\"}",
    "operation": "pretty"
}
```

## Package as Flink UDF

Use the ironfun CLI to package:

```bash
# Install ironfun (if not already installed)
curl -s https://irontools.dev/ironfun-cli-install.sh | sh

# Package as JAR
ironfun package-udf \
    --source-path . \
    --package-name com.demo.verify \
    --class-name VerifyExamples \
    --uber-jar
```

## Version Compatibility Verification

Run the version check script:

```bash
# From project root
python .scripts/iron-functions-tracker.py --check

# Update version records
python .scripts/iron-functions-tracker.py --update
```

## Troubleshooting

### Compilation Errors

**Error**: `error: no such target: wasm32-unknown-unknown`

Solution:

```bash
rustup target add wasm32-unknown-unknown
```

**Error**: `error: linking with cc failed`

Solution (macOS):

```bash
brew install llvm
```

### Runtime Errors

**Issue**: WASM module fails to load

Checklist:

1. Confirm `crate-type = ["cdylib"]` is used
2. Confirm `--release` mode is used for compilation
3. Check if module export function names are correct

## References

- [Iron Functions Documentation](https://irontools.dev/docs/)
- [Extism PDK Documentation](https://extism.org/docs/write-a-plugin/rust-pdk/)
- [Flink Integration Guide](../01-iron-functions-complete-guide.md)
